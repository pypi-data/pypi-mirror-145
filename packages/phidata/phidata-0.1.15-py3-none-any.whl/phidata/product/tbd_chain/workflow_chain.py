from datetime import datetime
from typing import Optional, List, Dict, Any

from phidata.product import DataProduct, DataProductArgs
from phidata.types.run_status import RunStatus
from phidata.workflow import Workflow
from phidata.utils.env_var import validate_env_vars
from phidata.utils.log import logger
from phidata.utils.cli_console import print_info, print_subheading, print_error


class WorkflowChainArgs(DataProductArgs):
    workflows: List[Workflow]


class WorkflowChain(DataProduct):
    def __init__(
        self,
        name: str,
        workflows: List[Workflow],
        # Optional: airflow dag_id for this WorkflowChain
        dag_id: Optional[str] = None,
        validate_env: Optional[Dict[str, Any]] = None,
        version: Optional[str] = None,
        enabled: bool = True,
    ) -> None:

        super().__init__()
        try:
            self.args: WorkflowChainArgs = WorkflowChainArgs(
                name=name,
                workflows=workflows,
                dag_id=dag_id,
                validate_env=validate_env,
                version=version,
                enabled=enabled,
            )
        except Exception as e:
            logger.error(f"Args for {self.__class__.__name__} are not valid")
            raise

    @property
    def workflows(self) -> Optional[List[Workflow]]:
        return self.args.workflows if self.args else None

    def run_in_local_env(self) -> bool:

        logger.debug("--**-- Running WorkflowChain locally")

        wf_run_status: List[RunStatus] = []
        for count, wf in enumerate(self.workflows, start=1):
            wf_name = wf.name or "{}__{}".format(wf.__class__.__name__, count)
            print_subheading(f"\nRunning {wf_name}")
            # logger.debug("Setting context")
            # Pass down context
            wf.run_context = self.run_context
            wf.path_context = self.path_context
            # Not required for local run but adding for posterity
            if self.dag_id:
                wf.dag_id = self.dag_id
            run_success = wf.run_in_local_env()
            wf_run_status.append(RunStatus(wf_name, run_success))

        print_subheading("\nWorkflow run status:")
        print_info(
            "\n".join(
                [
                    "{}: {}".format(wf.name, "Success" if wf.success else "Fail")
                    for wf in wf_run_status
                ]
            )
        )
        print_info("")
        for _run in wf_run_status:
            if not _run.success:
                return False
        return True

    def run_in_docker_container(self, active_container: Any) -> bool:

        logger.debug("--**-- Running WorkflowChain in docker container")

        wf_run_status: List[RunStatus] = []
        for count, wf in enumerate(self.workflows, start=1):
            wf_name = wf.name or "{}__{}".format(wf.__class__.__name__, count)
            print_subheading(f"\nRunning {wf_name}")
            # Pass down context
            wf.run_context = self.run_context
            wf.path_context = self.path_context
            wf.dag_id = self.dag_id
            run_success = wf.run_in_docker_container(active_container)
            wf_run_status.append(RunStatus(wf_name, run_success))

        print_subheading("\nWorkflow run status:")
        print_info(
            "\n".join(
                [
                    "{}: {}".format(wf.name, "Success" if wf.success else "Fail")
                    for wf in wf_run_status
                ]
            )
        )
        print_info("")
        for _run in wf_run_status:
            if not _run.success:
                return False
        return True

    def run_in_k8s_container(self) -> bool:
        logger.debug(f"@run_k8s not defined for {self.__class__.__name__}")
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
        # a dictionary of DAG level parameters that are made
        # accessible in templates, namespaced under `params`. These
        # params can be overridden at the task level.
        params: Optional[Dict] = None,
        # the number of task instances allowed to run concurrently
        concurrency: Optional[int] = None,
        # maximum number of active DAG runs, beyond this
        #  number of DAG runs in a running state, the scheduler won't create
        #  new active DAG runs
        max_active_runs: Optional[int] = None,
        doc_md: Optional[str] = None,
        is_paused_upon_creation: Optional[bool] = None,
        jinja_environment_kwargs: Optional[Dict] = None,
        tags: Optional[List[str]] = None,
    ) -> Any:
        """
        Used to create an Airflow DAG for this WorkflowChain.
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
            self.dag_id if self.dag_id else "default_dag_id",
            default_args=default_args,
            description=description,
            schedule_interval=schedule_interval,
            start_date=start_date,
            end_date=end_date,
        )
        for workflow in self.workflows:
            _add_task_success = workflow.add_airflow_tasks_to_dag(dag)
            if not _add_task_success:
                print_error(
                    "Tasks for workflow {} could not be added".format(workflow.name)
                )
        print_info(f"Airflow dag {dag_id} created")
        return dag
