"""
# TO independently test this module, you can run the example in the path
python examples/sklearn/iris_train.py

Besides running pytest
"""
import datetime
import logging
import os
import typing
import urllib
from functools import partial

import mlflow
import pandas as pd
from mlflow.entities import ViewType
from mlflow.store.artifact.artifact_repository_registry import (
    _artifact_repository_registry,
)
from mlflow.tracking import MlflowClient
from mlflow.tracking._tracking_service.utils import _get_default_host_creds

from mlfoundry import amplitude, constants
from mlfoundry.artifact.truefoundry_artifact_repo import TruefoundryArtifactRepository
from mlfoundry.exceptions import MlflowException, MlFoundryException
from mlfoundry.inference.store import (
    ActualPacket,
    InferencePacket,
    InferenceStoreClient,
    ValueType,
    get_inference_store,
)
from mlfoundry.internal_namespace import NAMESPACE
from mlfoundry.mlfoundry_run import MlFoundryRun
from mlfoundry.session import Session
from mlfoundry.tracking.auth_service import AuthService
from mlfoundry.tracking.truefoundry_rest_store import TruefoundryRestStore

log = logging.getLogger(__name__)


def init_rest_tracking(tracking_uri: str, api_key: typing.Optional[str]):
    get_cred = partial(_get_default_host_creds, tracking_uri)
    rest_store = TruefoundryRestStore(get_cred)
    auth_service = AuthService()

    session = Session(auth_service=auth_service, tracking_service=rest_store)
    session.init_session(api_key)

    artifact_repository = partial(TruefoundryArtifactRepository, rest_store=rest_store)
    _artifact_repository_registry.register("s3", artifact_repository)


def get_client(
    tracking_uri: typing.Optional[str] = None,
    inference_store_uri: typing.Optional[str] = None,
    disable_analytics: bool = False,
    api_key: typing.Optional[str] = None,
):
    amplitude.init(disable_analytics)
    if tracking_uri is None:
        tracking_uri = "file:" + os.path.abspath(constants.MLRUNS_FOLDER_NAME)
    elif tracking_uri.startswith("file:"):
        tracking_uri = os.path.join(tracking_uri, constants.MLRUNS_FOLDER_NAME)
    else:
        init_rest_tracking(tracking_uri=tracking_uri, api_key=api_key)
    amplitude.track(
        amplitude.Event.GET_CLIENT,
        # tracking whether user is using file:// or https://
        event_properties={
            "tracking_scheme": urllib.parse.urlparse(tracking_uri).scheme
        },
    )
    return MlFoundry(tracking_uri, inference_store_uri=inference_store_uri)


class MlFoundry:
    def __init__(
        self,
        tracking_uri: typing.Optional[str] = None,
        inference_store_uri: typing.Optional[str] = None,
    ):
        try:
            mlflow.set_tracking_uri(tracking_uri)
        except MlflowException as e:
            err_msg = (
                f"Could not initialise mlfoundry object. Error details: {e.message}"
            )
            raise MlFoundryException(err_msg) from e

        self.mlflow_client = MlflowClient()
        self.inference_store_client: typing.Optional[InferenceStoreClient] = (
            InferenceStoreClient(lambda: get_inference_store(inference_store_uri))
            if inference_store_uri is not None
            else None
        )

    def __get_or_create_experiment(self, experiment_name: str):
        """
        Creates a experiment and returns the experiment id. This experiment is to be passed into run.
        :param experiment_name: A unique experiment name
        :return: The experiment_id of created experiment

        Example:
        >> create_experiment('experiment 1')
        """

        try:
            experiment = self.mlflow_client.get_experiment_by_name(experiment_name)
            if experiment is None:
                experiment_id = self.mlflow_client.create_experiment(experiment_name)
            else:
                experiment_id = experiment.experiment_id
            return experiment_id
        except MlflowException as e:
            err_msg = (
                f"Error happened in creating or getting experiment based on experiment name: "
                f"{experiment_name}. Error details: {e.message}"
            )
            raise MlFoundryException(err_msg) from e

    def __construct_run_name(self, project_name: str, run_name=typing.Optional[str]):
        suffix = f"{datetime.datetime.utcnow().strftime(constants.TIME_FORMAT)}_utc"
        if run_name is None:
            return f"{constants.RUN_NAME_PREFIX}_{suffix}"
        # TODO: once we formalize how to keep run_name, use mlflow.search_runs
        all_runs_df = self.get_all_runs(project_name)
        if (
            not all_runs_df.empty
            and run_name in all_runs_df[constants.RUN_NAME_COL_NAME].values
        ):
            run_name = f"{run_name}_{suffix}"
        return run_name

    def get_all_projects(self):
        """
        Returns names of all the projects
        """
        amplitude.track(amplitude.Event.GET_ALL_PROJECTS)
        try:
            experiments = self.mlflow_client.list_experiments(view_type=ViewType.ALL)
        except MlflowException as e:
            err_msg = (
                f"Error happened in fetching project names. Error details: {e.message}"
            )
            raise MlFoundryException(err_msg) from e

        projects = []
        for e in experiments:
            # Experiment ID 0 represents default project which we are removing.
            if e.experiment_id != "0":
                projects.append(e.name)

        return projects

    def rename_project(self, old_project_name: str, new_project_name: str):
        """
        Renames a project.
        :param old_project_name: Existing project name
        :param new_project_name: New Project name
        """

        amplitude.track(amplitude.Event.RENAME_PROJECT)
        try:
            experiment_id = self.mlflow_client.get_experiment_by_name(
                old_project_name
            ).experiment_id

            self.mlflow_client.rename_experiment(experiment_id, new_project_name)
        except MlflowException as e:
            err_msg = (
                f"Error happened in renaming project from {old_project_name} to "
                f"{new_project_name}. Error details: {e.message}"
            )
            raise MlFoundryException(err_msg) from e

    def create_run(
        self,
        project_name: str,
        run_name: typing.Optional[str] = None,
        tags: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ) -> MlFoundryRun:
        """Creates a run for the given project_name(project_name).
        Each run will have a unique run_id.
        If run_name is not provided, then a name is generated automatically.
        Args:
            project_name (str): name of a project
            run_name (Optional[str]): name of the run
            tags (Optional: Dict[str, Any]): Tags to associate with this run
        Returns:
            MlFoundryRun: an MlFoundryRun with specified experiment and unique run_id

        Example:
        >> mlf_run = create_run('my_project')
        """

        amplitude.track(amplitude.Event.CREATE_RUN)
        if project_name == "" or (not isinstance(project_name, str)):
            raise MlFoundryException(
                f"project_name must be string type and not empty. "
                f"Got {type(project_name)} type with value {project_name}"
            )

        experiment_id = self.__get_or_create_experiment(project_name)
        run_name = self.__construct_run_name(project_name, run_name=run_name)

        if tags is not None:
            NAMESPACE.validate_namespace_not_used(tags.keys())
        else:
            tags = {}

        run = self.mlflow_client.create_run(
            experiment_id, tags={constants.RUN_NAME_COL_NAME: run_name, **tags}
        )
        mlf_run_id = run.info.run_id

        mlf_run = MlFoundryRun(experiment_id, mlf_run_id)
        mlf_run._add_git_info()
        log.info(f"Run is created with id {mlf_run_id} and name {run_name}")
        return mlf_run

    def get_run(self, run_id: str) -> MlFoundryRun:
        """Given the run_id returns the Python MlFoundryRun object that is created already.

        Args:
            run_id (str): run_id that was created already.

        Returns:
            MlFoundryRun: returns the run object that was created already.

        Example:
        >> run = get_run(<run_id>)
        """
        amplitude.track(amplitude.Event.GET_RUN)
        if run_id == "" or (not isinstance(run_id, str)):
            raise MlFoundryException(
                f"run_id must be string type and not empty. "
                f"Got {type(run_id)} type with value {run_id}"
            )

        run = self.mlflow_client.get_run(run_id)
        experiment_id = run.info.experiment_id
        return MlFoundryRun(experiment_id, run.info.run_id)

    def get_all_runs(self, project_name: str):
        """Returns all the run that was created by the user under the project project_name

        Returns:
            pd.DataFrame: dataframe with two columns- run_id and run_name
        """
        amplitude.track(amplitude.Event.GET_ALL_RUNS)
        if project_name == "" or (not isinstance(project_name, str)):
            raise MlFoundryException(
                f"project_name must be string type and not empty. "
                f"Got {type(project_name)} type with value {project_name}"
            )

        experiment_id = self.__get_or_create_experiment(project_name)

        try:
            all_run_infos = self.mlflow_client.list_run_infos(
                experiment_id, run_view_type=ViewType.ALL
            )
        except MlflowException as e:
            err_msg = f"Error happened in while fetching runs for project {project_name}. Error details: {e.message}"
            raise MlFoundryException(err_msg) from e

        runs = []

        for run_info in all_run_infos:
            try:
                run = self.mlflow_client.get_run(run_info.run_id)
                run_name = run.data.tags.get(constants.RUN_NAME_COL_NAME, "")
                runs.append((run_info.run_id, run_name))
            except MlflowException as e:
                log.warning(
                    f"Could not fetch details of run with run_id {run_info.run_id}. "
                    f"Skipping this one. Error details: {e.message}. "
                )

        return pd.DataFrame(
            runs, columns=[constants.RUN_ID_COL_NAME, constants.RUN_NAME_COL_NAME]
        )

    @staticmethod
    def get_tracking_uri():
        return mlflow.tracking.get_tracking_uri()

    def log_prediction(
        self,
        model_name: str,
        model_version: str,
        inference_id: str,
        features: ValueType,
        predictions: ValueType,
        raw_data: typing.Optional[ValueType] = None,
        actuals: typing.Optional[ValueType] = None,
        occurred_at: typing.Optional[int] = None,
    ):
        if self.inference_store_client is None:
            raise MlFoundryException(
                "Pass inference_store_uri in get_client function to use log_prediction"
            )
        if occurred_at is None:
            occurred_at = datetime.datetime.utcnow()
        elif not isinstance(occurred_at, int):
            raise TypeError("occurred_at should be unix epoch")
        else:
            occurred_at = datetime.datetime.utcfromtimestamp(occurred_at)
        inference_packet = InferencePacket(
            model_name=model_name,
            model_version=model_version,
            features=features,
            predictions=predictions,
            inference_id=inference_id,
            raw_data=raw_data,
            actuals=actuals,
            occurred_at=occurred_at,
        )
        self.inference_store_client.log_predictions([inference_packet])

    def log_actuals(self, model_name: str, inference_id: str, actuals: ValueType):
        if self.inference_store_client is None:
            raise MlFoundryException(
                "Pass inference_store_uri in get_client function to use log_prediction"
            )
        actuals_packet = ActualPacket(
            model_name=model_name, inference_id=inference_id, actuals=actuals
        )
        self.inference_store_client.log_actuals([actuals_packet])
