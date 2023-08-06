from collections import OrderedDict
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from typing_extensions import Literal

from phidata.app.db import DbApp
from phidata.app.databox.databox import Databox, DataboxArgs
from phidata.infra.docker.resource.container import DockerContainer
from phidata.infra.docker.resource.group import (
    DockerResourceGroup,
    DockerBuildContext,
)
from phidata.infra.k8s.enums.image_pull_policy import ImagePullPolicy
from phidata.infra.k8s.enums.restart_policy import RestartPolicy
from phidata.utils.cli_console import print_error, print_info
from phidata.utils.log import logger

default_devbox_name: str = "devbox"


class DevboxArgs(DataboxArgs):
    install_phidata_dev: bool = False
    phidata_volume_name: str = "devbox-phidata-volume"
    phidata_dir_path: Path = Path.home().joinpath("p", "philab", "phidata")
    phidata_dir_container_path: str = "/phidata"


class Devbox(Databox):
    def __init__(
        self,
        name: str = default_devbox_name,
        version: str = "1",
        enabled: bool = True,
        # Image args,
        image_name: str = "phidata/devbox",
        image_tag: str = "1",
        entrypoint: Optional[Union[str, List]] = None,
        command: Optional[Union[str, List]] = None,
        # Mount the workspace directory on the container,
        mount_workspace: bool = True,
        workspace_volume_name: str = "databox-ws-volume",
        # Path to mount the workspace volume under,
        # This is the parent directory for the workspace on the container,
        # i.e. the ws is mounted as a subdir in this dir,
        # eg: if ws name is: idata, workspace path would be: /usr/local/workspaces/idata,
        workspace_parent_container_path: str = "/usr/local/workspaces",
        # NOTE: On DockerContainers the workspace_root_path is mounted to workspace_dir,
        # because we assume that DockerContainers are running locally on the user's machine,
        # On K8sContainers, we load the workspace_dir from git using a git-sync sidecar container,
        create_git_sync_sidecar: bool = True,
        git_sync_repo: Optional[str] = None,
        git_sync_branch: Optional[str] = None,
        git_sync_wait: int = 1,
        # Install python dependencies using a requirements.txt file,
        install_requirements: bool = True,
        # Path to the requirements.txt file relative to the workspace root,
        requirements_file_path: str = "requirements.txt",
        # Only on DockerContainers, for K8sContainers use IamRole
        # Mount aws config on the container
        mount_aws_config: bool = False,
        # Aws config dir on the host,
        aws_config_path: Path = Path.home().resolve().joinpath(".aws"),
        # Aws config dir on the container,
        aws_config_container_path: str = "/root/.aws",
        # Only on DockerContainers,
        # Mount airflow home from container to host machine,
        # Useful when debugging the airflow conf,
        mount_airflow_home: bool = False,
        # Path to the dir on host machine relative to the workspace root,
        airflow_home_dir: str = "airflow",
        # Path to airflow home on the container,
        airflow_home_container_path: str = "/usr/local/airflow",
        # Configure airflow,
        # If init_airflow = True, this databox initializes airflow and,
        # add env var INIT_AIRFLOW = True which is required by phidata to build dags,
        init_airflow: bool = True,
        # If use_products_as_airflow_dags = True,
        # set the AIRFLOW__CORE__DAGS_FOLDER to the products_dir,
        use_products_as_airflow_dags: bool = True,
        # If use_products_as_airflow_dags = False,
        # set the AIRFLOW__CORE__DAGS_FOLDER to the airflow_dags_path,
        # airflow_dags_path is the directory in the container containing the airflow dags,
        airflow_dags_path: Optional[str] = None,
        # Creates an airflow user with username: test, pass: test,
        create_airflow_test_user: bool = False,
        airflow_executor: Literal[
            "DebugExecutor",
            "LocalExecutor",
            "SequentialExecutor",
            "CeleryExecutor",
            "CeleryKubernetesExecutor",
            "DaskExecutor",
            "KubernetesExecutor",
        ] = "SequentialExecutor",
        logging_level: Literal[
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        ] = "INFO",
        # Configure airflow db,
        # If True, initialize the airflow_db on this databox,
        # If None, value is derived from init_airflow i.e. initialize the airflow_db if init_airflow = True,
        #   Locally, airflow_db uses sqllite,
        # If using the databox with an external Airflow db, set init_airflow_db = False,
        init_airflow_db: Optional[bool] = None,
        wait_for_airflow_db: bool = False,
        # Connect to database using DbApp,
        airflow_db_app: Optional[DbApp] = None,
        # Connect to database manually,
        airflow_db_user: Optional[str] = None,
        airflow_db_password: Optional[str] = None,
        airflow_db_schema: Optional[str] = None,
        airflow_db_host: Optional[str] = None,
        airflow_db_port: Optional[str] = None,
        airflow_db_driver: str = "postgresql+psycopg2",
        # Airflow db connections in the format { conn_id: conn_url },
        # converted to env var: AIRFLOW_CONN__conn_id = conn_url,
        db_connections: Optional[Dict] = None,
        # Configure airflow scheduler,
        # Init Airflow scheduler as a daemon process,
        init_airflow_scheduler: bool = False,
        # Configure airflow webserver,
        # Init Airflow webserver when the container starts,
        init_airflow_webserver: bool = False,
        # Open the port if init_airflow_webserver=True,
        # webserver port on the container,
        airflow_webserver_container_port: int = 8080,
        # webserver port on the host machine,
        airflow_webserver_host_port: int = 8080,
        # webserver port name on K8sContainer,
        airflow_webserver_port_name: str = "http",
        # Configure the container,
        container_name: Optional[str] = None,
        image_pull_policy: ImagePullPolicy = ImagePullPolicy.IF_NOT_PRESENT,
        # Only used by the DockerContainer,
        container_detach: bool = True,
        container_auto_remove: bool = True,
        container_remove: bool = True,
        # Add env variables to container env,
        env: Optional[Dict[str, str]] = None,
        # Read env variables from a file in yaml format,
        env_file: Optional[Path] = None,
        # Configure the ConfigMap used for env variables that are not Secret,
        config_map_name: Optional[str] = None,
        # Configure the Secret used for env variables that are Secret,
        secret_name: Optional[str] = None,
        # Read secrets from a file in yaml format,
        secrets_file: Optional[Path] = None,
        # Configure the databox deploy,
        deploy_name: Optional[str] = None,
        pod_name: Optional[str] = None,
        replicas: int = 1,
        pod_node_selector: Optional[Dict[str, str]] = None,
        restart_policy: RestartPolicy = RestartPolicy.ALWAYS,
        termination_grace_period_seconds: Optional[int] = None,
        # Other args,
        load_examples: bool = False,
        print_env_on_load: bool = True,
        # Additional args
        # If True, skip resource creation if active resources with the same name exist.
        use_cache: bool = True,
        # If True, log extra debug messages
        use_verbose_logs: bool = False,
        install_phidata_dev: bool = False,
        phidata_volume_name: str = "devbox-phidata-volume",
        phidata_dir_path: Path = Path.home().joinpath("p", "philab", "phidata"),
        phidata_dir_container_path: str = "/phidata",
    ):
        super().__init__()
        try:
            self.args: DevboxArgs = DevboxArgs(
                name=name,
                version=version,
                enabled=enabled,
                image_name=image_name,
                image_tag=image_tag,
                entrypoint=entrypoint,
                command=command,
                mount_workspace=mount_workspace,
                workspace_volume_name=workspace_volume_name,
                workspace_parent_container_path=workspace_parent_container_path,
                create_git_sync_sidecar=create_git_sync_sidecar,
                git_sync_repo=git_sync_repo,
                git_sync_branch=git_sync_branch,
                git_sync_wait=git_sync_wait,
                install_requirements=install_requirements,
                requirements_file_path=requirements_file_path,
                mount_aws_config=mount_aws_config,
                aws_config_path=aws_config_path,
                aws_config_container_path=aws_config_container_path,
                mount_airflow_home=mount_airflow_home,
                airflow_home_dir=airflow_home_dir,
                airflow_home_container_path=airflow_home_container_path,
                init_airflow=init_airflow,
                use_products_as_airflow_dags=use_products_as_airflow_dags,
                airflow_dags_path=airflow_dags_path,
                create_airflow_test_user=create_airflow_test_user,
                airflow_executor=airflow_executor,
                logging_level=logging_level,
                init_airflow_db=init_airflow_db,
                wait_for_airflow_db=wait_for_airflow_db,
                airflow_db_app=airflow_db_app,
                airflow_db_user=airflow_db_user,
                airflow_db_password=airflow_db_password,
                airflow_db_schema=airflow_db_schema,
                airflow_db_host=airflow_db_host,
                airflow_db_port=airflow_db_port,
                airflow_db_driver=airflow_db_driver,
                db_connections=db_connections,
                init_airflow_scheduler=init_airflow_scheduler,
                init_airflow_webserver=init_airflow_webserver,
                airflow_webserver_container_port=airflow_webserver_container_port,
                airflow_webserver_host_port=airflow_webserver_host_port,
                airflow_webserver_port_name=airflow_webserver_port_name,
                container_name=container_name,
                image_pull_policy=image_pull_policy,
                container_detach=container_detach,
                container_auto_remove=container_auto_remove,
                container_remove=container_remove,
                env=env,
                env_file=env_file,
                config_map_name=config_map_name,
                secret_name=secret_name,
                secrets_file=secrets_file,
                deploy_name=deploy_name,
                pod_name=pod_name,
                replicas=replicas,
                pod_node_selector=pod_node_selector,
                restart_policy=restart_policy,
                termination_grace_period_seconds=termination_grace_period_seconds,
                load_examples=load_examples,
                print_env_on_load=print_env_on_load,
                use_cache=use_cache,
                use_verbose_logs=use_verbose_logs,
                install_phidata_dev=install_phidata_dev,
                phidata_volume_name=phidata_volume_name,
                phidata_dir_path=phidata_dir_path,
                phidata_dir_container_path=phidata_dir_container_path,
            )
        except Exception as e:
            logger.error(f"Args for {self.__class__.__name__} are not valid")
            raise

    ######################################################
    ## Docker Resources
    ######################################################

    def get_docker_rg(
        self, docker_build_context: DockerBuildContext
    ) -> Optional[DockerResourceGroup]:

        databox_docker_rg = super().get_docker_rg(docker_build_context)
        container_to_update: Optional[DockerContainer] = None
        container_name = self.get_container_name()
        for idx, container in enumerate(databox_docker_rg.containers, start=0):
            if container.name == container_name:
                container_to_update = databox_docker_rg.containers.pop(idx)

        if container_to_update is None:
            print_error("No databox container")
            return None
        # logger.debug(f"Updating container: {container_to_update}")

        # Install phidata in dev mode
        if self.args.install_phidata_dev:
            # Update container environment
            container_env: Dict[str, Any] = {
                "INSTALL_PHIDATA_DEV": str(self.args.install_phidata_dev),
                "PHIDATA_DIR_PATH": self.args.phidata_dir_container_path,
            }
            container_to_update.environment.update(container_env)

            # Create a volume for phidata dev
            if self.args.phidata_dir_path is not None:
                phidata_dir_absolute_path_str = str(self.args.phidata_dir_path)
                logger.debug(f"Mounting: {phidata_dir_absolute_path_str}")
                logger.debug(f"\tto: {self.args.phidata_dir_container_path}")
                container_to_update.volumes[phidata_dir_absolute_path_str] = {
                    "bind": self.args.phidata_dir_container_path,
                    "mode": "rw",
                }
        databox_docker_rg.containers.append(container_to_update)
        return databox_docker_rg

    def init_docker_resource_groups(
        self, docker_build_context: DockerBuildContext
    ) -> None:
        docker_rg = self.get_docker_rg(docker_build_context)
        if docker_rg is not None:
            if self.docker_resource_groups is None:
                self.docker_resource_groups = OrderedDict()
            self.docker_resource_groups[docker_rg.name] = docker_rg
