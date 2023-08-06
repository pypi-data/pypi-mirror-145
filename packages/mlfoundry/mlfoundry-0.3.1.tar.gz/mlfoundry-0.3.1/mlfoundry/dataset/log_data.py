import collections
import json
import os
import tempfile
import typing

import numpy as np
import pandas as pd
from pandas.api.types import infer_dtype

from mlfoundry import constants
from mlfoundry.dataset.enums import DataSet, DataSetType, Schema
from mlfoundry.enums import DataSlice, FieldType, FileFormat, ModelFramework, ModelType
from mlfoundry.exceptions import MlflowException, MlFoundryException
from mlfoundry.mlfoundry_run import MlFoundryRun

CATEGORICAL_PANDAS_TYPES = ["categorical", "boolean"]
NUMERICAL_PANDAS_TYPES = ["integer", "floating", "mixed-integer-float"]
MIXED_INTEGER_OR_FLOAT_PANDAS_TYPES = [
    "floating",
    "mixed-integer-float",
    "mixed-integer",
]
MIXED_PANDAS_TYPES = ["mixed", "mixed-integer"]
SCHEMA_FILENAME = "schema.json"


def convert_to_pandas_series(x):
    if x is None or isinstance(x, pd.Series):
        return x
    elif isinstance(x, list) or (isinstance(x, np.ndarray) and x.ndim == 1):
        return pd.Series(x)
    else:
        raise MlFoundryException(
            f"Not a valid input data type. Should be one of pandas.Series, list, numpy 1D array. Received {type(x)}"
        )


def is_categorial(features) -> bool:
    inferred_dtype = infer_dtype(features)
    if inferred_dtype in MIXED_INTEGER_OR_FLOAT_PANDAS_TYPES:
        return False
    if inferred_dtype in CATEGORICAL_PANDAS_TYPES:
        return True
    return False


def is_mixed_type(features) -> bool:
    if features.isnull().any():
        return True
    inferred_dtype = infer_dtype(features)
    if inferred_dtype in MIXED_PANDAS_TYPES:
        return True
    return False


def is_numerical(features) -> bool:
    inferred_dtype = infer_dtype(features)
    if inferred_dtype not in NUMERICAL_PANDAS_TYPES:
        return False
    return True


def validate_fieldtype(data, fieldtype):
    if is_mixed_type(data):
        return False
    if fieldtype == FieldType.NUMERICAL and is_numerical(data):
        return True
    if fieldtype == FieldType.CATEGORICAL and is_categorial(data):
        return True
    return False


def validate_dataset(
    schema: Schema,
    features: pd.DataFrame,
    actuals,
    predictions=None,
):
    feature_columns_absent_in_df = schema.features.keys() - set(features.columns)
    if len(feature_columns_absent_in_df) > 0:
        raise MlFoundryException(
            f"{feature_columns_absent_in_df} not present in features dataframe."
        )

    if features.shape[0] != len(actuals):
        raise MlFoundryException(
            f"Features (length {len(features)}) and Actuals (length {len(actuals)}) are not of the same length."
        )

    if predictions is not None and features.shape[0] != len(predictions):
        raise MlFoundryException(
            f"Features (length {len(features)}) and Predictions (length {len(predictions)}) are not of the same length."
        )

    for feature_name, feature_fieldtype in schema.features.items():
        if not validate_fieldtype(features[feature_name], feature_fieldtype):
            raise MlFoundryException(
                f"{feature_name} is not of type {feature_fieldtype}."
            )
    actuals_fieldtype = schema.actuals
    if not validate_fieldtype(actuals, actuals_fieldtype):
        raise MlFoundryException(
            f"{DataSetType.ACTUALS.value} is not of {actuals_fieldtype}."
        )
    if predictions is not None and not validate_fieldtype(
        predictions, actuals_fieldtype
    ):
        raise MlFoundryException(
            f"{DataSetType.PREDICTIONS.value} is not of {actuals_fieldtype}."
        )


def is_already_logged_dataset(mlflow_client, run_id, data_slice: DataSlice):
    artifacts = mlflow_client.list_artifacts(run_id, constants.LOG_DATASET_ARTIFACT_DIR)
    for artifact in artifacts:
        if get_log_dataset_filename(data_slice, DataSetType.FEATURES) in artifact.path:
            raise MlFoundryException(
                f"Exception: {data_slice.value} dataset for Run {str(run_id)} already logged, can't be overwritten."
            )


def get_log_dataset_filename(
    data_slice: DataSlice,
    dataset_type: DataSetType,
    fileformat: FileFormat = None,
):
    if fileformat:
        return data_slice.value + "_" + dataset_type.value + "." + str(fileformat.value)
    else:
        return data_slice.value + "_" + dataset_type.value


def log_dataset(
    mlflow_client,
    run_id,
    data_slice: DataSlice,
    schema: Schema,
    features: pd.DataFrame,
    actuals,
    predictions=None,
    file_format: FileFormat = FileFormat.PARQUET,
    only_stats: bool = False,
):

    actuals = convert_to_pandas_series(actuals)
    predictions = convert_to_pandas_series(predictions)

    validate_dataset(schema, features, actuals, predictions)
    is_already_logged_dataset(mlflow_client, run_id, data_slice)

    with tempfile.TemporaryDirectory() as tmpdirname:
        features_filepath = os.path.join(
            tmpdirname,
            get_log_dataset_filename(data_slice, DataSetType.FEATURES, file_format),
        )
        actuals_filepath = os.path.join(
            tmpdirname,
            get_log_dataset_filename(data_slice, DataSetType.ACTUALS, file_format),
        )
        predictions_filepath = os.path.join(
            tmpdirname,
            get_log_dataset_filename(data_slice, DataSetType.PREDICTIONS, file_format),
        )
        schema_filepath = os.path.join(tmpdirname, SCHEMA_FILENAME)
        with open(schema_filepath, "w") as schema_file:
            schema_file.write(schema.json())

        if file_format == FileFormat.PARQUET:
            features.to_parquet(features_filepath, index=False)
            actuals.to_frame(name=DataSetType.ACTUALS.value).to_parquet(
                actuals_filepath, index=False
            )
            if predictions is not None:
                predictions.to_frame(name=DataSetType.PREDICTIONS.value).to_parquet(
                    predictions_filepath, index=False
                )

        elif file_format == FileFormat.CSV:
            features.to_csv(features_filepath, index=False)
            actuals.to_csv(actuals_filepath, index=False)
            if predictions is not None:
                predictions.to_csv(predictions_filepath, index=False)

        else:
            raise MlFoundryException(
                f"Not a valid file format. Should be one of Parquet or CSV. Received {file_format}"
            )

        try:
            mlflow_client.log_artifacts(
                run_id, tmpdirname, constants.LOG_DATASET_ARTIFACT_DIR
            )
        except MlflowException as e:
            raise MlFoundryException(e.message).with_traceback(
                e.__traceback__
            ) from None


def download_dataset_file(
    mlflow_client,
    run_id,
    data_slice: DataSlice,
    dataset_type: DataSetType,
    tmpdirname,
):
    if dataset_type == DataSetType.SCHEMA:
        artifact_name = SCHEMA_FILENAME
    else:
        artifact_name = get_log_dataset_filename(data_slice, dataset_type)

    artifacts = mlflow_client.list_artifacts(run_id, constants.LOG_DATASET_ARTIFACT_DIR)
    for artifact in artifacts:
        if artifact_name in artifact.path:
            return mlflow_client.download_artifacts(run_id, artifact.path, tmpdirname)
    return None


def get_dataset(data_slice: DataSlice, mlflow_client, run_id) -> DataSet:
    """
    Returns the dataset
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        features_filepath = download_dataset_file(
            mlflow_client, run_id, data_slice, DataSetType.FEATURES, tmpdirname
        )
        actuals_filepath = download_dataset_file(
            mlflow_client, run_id, data_slice, DataSetType.ACTUALS, tmpdirname
        )
        predictions_filepath = download_dataset_file(
            mlflow_client, run_id, data_slice, DataSetType.PREDICTIONS, tmpdirname
        )
        schema_filepath = download_dataset_file(
            mlflow_client, run_id, data_slice, DataSetType.SCHEMA, tmpdirname
        )

        predictions = None
        if not features_filepath:
            raise MlFoundryException("Dataset not logged!")

        with open(schema_filepath, "r") as schema_file:
            schema = Schema(**json.loads(schema_file.read()))

        ext = features_filepath.split(".")[-1]

        if ext == FileFormat.PARQUET.value:
            features = pd.read_parquet(features_filepath)
            actuals = pd.read_parquet(actuals_filepath).squeeze()
            if predictions_filepath:
                predictions = pd.read_parquet(predictions_filepath).squeeze()

        elif ext == FileFormat.CSV.value:
            features = pd.read_csv(features_filepath)
            actuals = pd.read_csv(actuals_filepath).squeeze()
            if predictions_filepath:
                predictions = pd.read_csv(predictions_filepath).squeeze()

        else:
            raise MlFoundryException(
                f'Not a valid file extension. Should be one of ".parquet" or ".csv". Received ".{ext}"'
            )

        dataset = DataSet(
            features=features,
            actuals=actuals,
            predictions=predictions,
            dataset_schema=schema,
        )
        return dataset
