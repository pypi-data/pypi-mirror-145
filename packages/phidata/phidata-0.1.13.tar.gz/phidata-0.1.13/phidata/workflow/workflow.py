from datetime import datetime
from pathlib import Path
from typing import Optional, Any, Dict, List

from pydantic import BaseModel

from phidata.constants import (
    SCRIPTS_DIR_ENV_VAR,
    STORAGE_DIR_ENV_VAR,
    META_DIR_ENV_VAR,
    PRODUCTS_DIR_ENV_VAR,
    NOTEBOOKS_DIR_ENV_VAR,
    WORKSPACE_CONFIG_DIR_ENV_VAR,
)
from phidata.utils.cli_console import print_info, print_error
from phidata.utils.env_var import validate_env_vars
from phidata.utils.log import logger
from phidata.types.context import PathContext, RunContext


class WorkflowArgs(BaseModel):
    name: str
    version: Optional[str] = None
    enabled: bool = True

    # Optional: airflow task_id for this workflow, use name if not provided
    task_id: Optional[str] = None
    # Optional: airflow dag_id for this workflow, use name if not provided
    dag_id: Optional[str] = None
    # run_context is provided by wf_operator
    run_context: Optional[RunContext] = None
    # path_context is provided using env variables
    path_context: Optional[PathContext] = None

    # ENV variables to validate before running the workflow
    validate_env: Optional[Dict[str, Any]] = None
    # Validate airflow is active on the containers
    validate_airflow_env: Dict[str, Any] = {"INIT_AIRFLOW": True}

    class Config:
        arbitrary_types_allowed = True


class Workflow:
    """Base Class for all Workflows"""

    def __init__(self) -> None:
        self.args: Optional[WorkflowArgs] = None

    @property
    def name(self) -> str:
        return self.args.name if self.args else self.__class__.__name__

    @property
    def version(self) -> Optional[str]:
        return self.args.version if self.args else None

    @property
    def enabled(self) -> bool:
        return self.args.enabled if self.args else False

    @property
    def task_id(self) -> str:
        return self.args.task_id if (self.args and self.args.task_id) else self.name

    @task_id.setter
    def task_id(self, task_id: str) -> None:
        if self.args is not None and task_id is not None:
            self.args.task_id = task_id

    @property
    def dag_id(self) -> str:
        return self.args.dag_id if (self.args and self.args.dag_id) else self.name

    @dag_id.setter
    def dag_id(self, dag_id: str) -> None:
        if self.args is not None and dag_id is not None:
            self.args.dag_id = dag_id

    @property
    def run_context(self) -> Optional[RunContext]:
        return self.args.run_context if self.args else None

    @run_context.setter
    def run_context(self, run_context: RunContext) -> None:
        if self.args is not None and run_context is not None:
            self.args.run_context = run_context

    @property
    def path_context(self) -> Optional[PathContext]:
        # Workflow not yet initialized
        if self.args is None:
            return None

        if self.args.path_context is not None:
            # use cached value if available
            return self.args.path_context

        logger.debug(f"--++**++--> Loading PathContext from env")
        self.path_context = PathContext()

        import os

        scripts_dir = os.getenv(SCRIPTS_DIR_ENV_VAR)
        storage_dir = os.getenv(STORAGE_DIR_ENV_VAR)
        meta_dir = os.getenv(META_DIR_ENV_VAR)
        products_dir = os.getenv(PRODUCTS_DIR_ENV_VAR)
        notebooks_dir = os.getenv(NOTEBOOKS_DIR_ENV_VAR)
        workspace_config_dir = os.getenv(WORKSPACE_CONFIG_DIR_ENV_VAR)

        if storage_dir is None:
            print_error(f"{STORAGE_DIR_ENV_VAR} not set")
        if products_dir is None:
            print_error(f"{PRODUCTS_DIR_ENV_VAR} not set")

        try:
            if scripts_dir is not None:
                self.path_context.scripts_dir = Path(scripts_dir)
            if storage_dir is not None:
                self.path_context.storage_dir = Path(storage_dir)
            if meta_dir is not None:
                self.path_context.meta_dir = Path(meta_dir)
            if products_dir is not None:
                self.path_context.products_dir = Path(products_dir)
            if notebooks_dir is not None:
                self.path_context.notebooks_dir = Path(notebooks_dir)
            if workspace_config_dir is not None:
                self.path_context.workspace_config_dir = Path(workspace_config_dir)
        except Exception as e:
            raise
        logger.debug(f"--++**++--> PathContext loaded")
        return self.args.path_context

    @path_context.setter
    def path_context(self, path_context: PathContext) -> None:
        if self.args is not None and path_context is not None:
            self.args.path_context = path_context

    @property
    def validate_env(self) -> Optional[Dict[str, Any]]:
        return self.args.validate_env if self.args else None

    @validate_env.setter
    def validate_env(self, validate_env: Optional[Dict[str, Any]]) -> None:
        if self.args is not None and validate_env is not None:
            self.args.validate_env = validate_env

    @property
    def validate_airflow_env(self) -> Dict[str, Any]:
        return self.args.validate_airflow_env if self.args else None

    @validate_airflow_env.setter
    def validate_airflow_env(self, validate_airflow_env: Dict[str, Any]) -> None:
        if self.args is not None and validate_airflow_env is not None:
            self.args.validate_airflow_env = validate_airflow_env

    ######################################################
    ## Build and validate workflow
    ######################################################

    def build(self) -> bool:
        logger.debug(f"@build not defined for {self.__class__.__name__}")
        return False

    ######################################################
    ## Run workflow
    ######################################################

    def run_in_local_env(self) -> bool:
        """
        Runs a workflow in the local environment where phi wf is called from.

        Returns:
            run_status (bool): True if the run was successful
        """
        logger.debug(f"@run_in_local_env not defined for {self.__class__.__name__}")
        return False

    def run_in_docker_container(
        self, active_container: Any, docker_env: Optional[Dict[str, str]] = None
    ) -> bool:
        """
        Runs a workflow in a docker container.

        Args:
            active_container:
            docker_env:

        Returns:
            run_status (bool): True if the run was successful

        Notes:
            * This function runs in the local environment where phi wf is called from.
            But executes `airflow` commands in the docker container to run the workflow
            * For the airflow tasks to be available, they need to be added to the workflow DAG
            using add_airflow_tasks_to_dag()
        """
        logger.debug(
            f"@run_in_docker_container not defined for {self.__class__.__name__}"
        )
        return False

    def run_in_k8s_container(
        self,
        pod: Any,
        k8s_api_client: Any,
        container_name: Optional[str] = None,
        k8s_env: Optional[Dict[str, str]] = None,
    ) -> bool:
        logger.debug(f"@run_in_k8s_container not defined for {self.__class__.__name__}")
        return False

    ######################################################
    ## Airflow functions
    ######################################################

    def add_airflow_tasks_to_dag(self, dag: Any) -> bool:
        """
        Add tasks to the airflow DAG.

        Args:
            dag:

        Returns:

        Notes:
            * This function is called as part of the create_airflow_dag() function
        """
        logger.debug(
            f"@add_airflow_tasks_to_dag not defined for {self.__class__.__name__}"
        )
        return False

    def create_airflow_dag(
        self,
        owner: Optional[str] = "airflow",
        depends_on_past: Optional[bool] = False,
        # The description for the DAG to e.g. be shown on the webserver
        description: Optional[str] = None,
        # Defines how often that DAG runs, this
        #  timedelta object gets added to your latest task instance's
        #  execution_date to figure out the next schedule
        schedule_interval: Optional[Any] = None,
        # The timestamp from which the scheduler will
        #  attempt to backfill
        start_date: Optional[datetime] = None,
        # A date beyond which your DAG won't run, leave to None
        #  for open ended scheduling
        end_date: Optional[datetime] = None,
        # a dictionary of macros that will be exposed
        #  in your jinja templates. For example, passing ``dict(foo='bar')``
        #  to this argument allows you to ``{{ foo }}`` in all jinja
        #  templates related to this DAG. Note that you can pass any
        #  type of object here.
        user_defined_macros: Optional[Dict] = None,
        # a dictionary of filters that will be exposed
        #  in your jinja templates. For example, passing
        #  ``dict(hello=lambda name: 'Hello %s' % name)`` to this argument allows
        #  you to ``{{ 'world' | hello }}`` in all jinja templates related to
        #  this DAG.
        user_defined_filters: Optional[Dict] = None,
        # A dictionary of default parameters to be used
        #  as constructor keyword parameters when initialising operators.
        #  Note that operators have the same hook, and precede those defined
        #  here, meaning that if your dict contains `'depends_on_past': True`
        #  here and `'depends_on_past': False` in the operator's call
        #  `default_args`, the actual value will be `False`.
        default_args: Optional[Dict] = None,
        # the number of task instances allowed to run concurrently
        concurrency: Optional[int] = None,
        # maximum number of active DAG runs, beyond this
        #  number of DAG runs in a running state, the scheduler won't create
        #  new active DAG runs
        max_active_runs: int = 8,
        doc_md: Optional[str] = None,
        # a dictionary of DAG level parameters that are made
        # accessible in templates, namespaced under `params`. These
        # params can be overridden at the task level.
        params: Optional[Dict] = None,
        is_paused_upon_creation: Optional[bool] = None,
        jinja_environment_kwargs: Optional[Dict] = None,
        tags: Optional[List[str]] = None,
    ) -> Any:
        """
        Used to create an Airflow DAG for independent workflows.
        It is preferred to create 1 DAG for each DataProduct but not all pipelines
        have DataProducts, some just have 1 Workflow.
        """
        if not validate_env_vars(self.args.validate_airflow_env):
            # This function skips DAG creation on local machines
            # print_error(f"Could not validate airflow env: {self.args.validate_airflow_env}")
            return None

        from airflow import DAG
        from airflow.utils.dates import days_ago

        default_args = {
            "owner": owner,
            "depends_on_past": depends_on_past,
        }
        if start_date is None:
            start_date = days_ago(3)

        dag_id = self.dag_id
        if dag_id is None:
            print_error("Workflow dag_id unavailable")
            return False
        dag = DAG(
            dag_id=dag_id,
            description=description,
            schedule_interval=schedule_interval,
            start_date=start_date,
            end_date=end_date,
            user_defined_macros=user_defined_macros,
            user_defined_filters=user_defined_filters,
            default_args=default_args,
            concurrency=concurrency,
            max_active_runs=max_active_runs,
            doc_md=doc_md,
            params=params,
            is_paused_upon_creation=is_paused_upon_creation,
            jinja_environment_kwargs=jinja_environment_kwargs,
            tags=tags,
        )
        add_task_success = self.add_airflow_tasks_to_dag(dag)
        if not add_task_success:
            print_error("Tasks for workflow {} could not be added".format(self.name))
        logger.debug(f"Airflow dag {dag_id} created")
        return dag
