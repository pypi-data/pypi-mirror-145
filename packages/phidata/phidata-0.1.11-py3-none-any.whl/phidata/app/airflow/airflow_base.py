from collections import OrderedDict
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from typing_extensions import Literal

from phidata.app.db import DbApp
from phidata.app import PhidataApp, PhidataAppArgs
from phidata.infra.docker.resource.network import DockerNetwork
from phidata.infra.docker.resource.container import DockerContainer
from phidata.infra.docker.resource.group import (
    DockerResourceGroup,
    DockerBuildContext,
)
from phidata.infra.k8s.create.apps.v1.deployment import CreateDeployment, RestartPolicy
from phidata.infra.k8s.create.core.v1.secret import CreateSecret
from phidata.infra.k8s.create.core.v1.service import CreateService, ServiceType
from phidata.infra.k8s.create.core.v1.config_map import CreateConfigMap
from phidata.infra.k8s.create.core.v1.container import CreateContainer, ImagePullPolicy
from phidata.infra.k8s.create.core.v1.volume import (
    CreateVolume,
    VolumeType,
)
from phidata.infra.k8s.create.common.port import CreatePort
from phidata.infra.k8s.create.group import CreateK8sResourceGroup
from phidata.infra.k8s.resource.group import (
    K8sResourceGroup,
    K8sBuildContext,
)
from phidata.utils.common import (
    get_image_str,
    get_default_container_name,
    get_default_configmap_name,
    get_default_secret_name,
    get_default_service_name,
    get_default_deploy_name,
    get_default_pod_name,
)
from phidata.utils.cli_console import print_error
from phidata.utils.log import logger


class AirflowBaseArgs(PhidataAppArgs):
    name: str = "airflow"
    version: str = "1"
    enabled: bool = True

    # Image args
    image_name: str = "phidata/airflow"
    image_tag: str = "1"
    entrypoint: Optional[Union[str, List]] = None
    command: Optional[Union[str, List]] = None

    # Mount the workspace directory on the container
    mount_workspace: bool = True
    workspace_volume_name: str = "airflow-ws-volume"
    # Path to mount the workspace volume under
    # This is the parent directory for the workspace on the container
    # i.e. the ws is mounted as a subdir in this dir
    # eg: if ws name is: idata, workspace_dir would be: /usr/local/workspaces/idata
    workspace_parent_container_path: str = "/usr/local/workspaces"
    # NOTE: On DockerContainers the workspace_root_path is mounted to workspace_dir
    # because we assume that DockerContainers are running locally on the user's machine
    # On K8sContainers, we load the workspace_dir from git using a git-sync sidecar container
    create_git_sync_sidecar: bool = True
    git_sync_repo: Optional[str] = None
    git_sync_branch: Optional[str] = None
    git_sync_wait: int = 1

    # Install python dependencies using a requirements.txt file
    install_requirements: bool = True
    # Path to the requirements.txt file relative to the workspace root
    requirements_file_path: str = "requirements.txt"

    # Mount aws config on the container
    # Only on DockerContainers, for K8sContainers use IamRole
    mount_aws_config: bool = False
    aws_config_volume_name: str = "airflow-aws-config-volume"
    # Aws config dir on the host
    aws_config_path: Path = Path.home().resolve().joinpath(".aws")
    # Aws config dir on the container
    aws_config_container_path: str = "/root/.aws"

    # Configure airflow
    # If use_products_as_airflow_dags = True
    # set the AIRFLOW__CORE__DAGS_FOLDER to the products_dir
    use_products_as_airflow_dags: bool = True
    # If use_products_as_airflow_dags = False
    # set the AIRFLOW__CORE__DAGS_FOLDER to the airflow_dags_path
    # airflow_dags_path is the directory in the container containing the airflow dags
    airflow_dags_path: Optional[str] = None
    # Creates an airflow user with username: test, pass: test
    create_airflow_test_user: bool = False
    executor: Literal[
        "DebugExecutor",
        "LocalExecutor",
        "SequentialExecutor",
        "CeleryExecutor",
        "CeleryKubernetesExecutor",
        "DaskExecutor",
        "KubernetesExecutor",
    ] = "SequentialExecutor"
    logging_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"

    # Configure airflow db
    # If init_airflow_db = True, initialize the airflow_db
    init_airflow_db: bool = False
    wait_for_db: bool = False
    # Connect to database using DbApp
    db_app: Optional[DbApp] = None
    # Connect to database manually
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    db_schema: Optional[str] = None
    db_host: Optional[str] = None
    db_port: Optional[str] = None
    db_driver: str = "postgresql+psycopg2"
    # Airflow db connections in the format { conn_id: conn_url }
    # converted to env var: AIRFLOW_CONN__conn_id = conn_url
    db_connections: Optional[Dict] = None

    # Configure airflow redis
    wait_for_redis: bool = False
    # Connect to redis using PhidataApp
    redis_app: Optional[Any] = None
    # Connect to redis manually
    redis_user: Optional[str] = None
    redis_password: Optional[str] = None
    redis_schema: Optional[str] = None
    redis_host: Optional[str] = None
    redis_port: Optional[str] = None

    # Configure the container
    container_name: Optional[str] = None
    image_pull_policy: ImagePullPolicy = ImagePullPolicy.IF_NOT_PRESENT
    # Open the container port if create_port=True
    # Used by the airflow-webserver
    create_port: bool = False
    container_port: int = 8080
    # Only used by the K8sContainer
    container_port_name: str = "http"
    # Only used by the DockerContainer
    container_host_port: int = 8080
    container_detach: bool = True
    container_auto_remove: bool = True
    container_remove: bool = True

    # Add env variables to container env
    env: Optional[Dict[str, str]] = None
    # Read env variables from a file in yaml format
    env_file: Optional[Path] = None
    # Configure the ConfigMap used for env variables that are not Secret
    config_map_name: Optional[str] = None
    # Configure the Secret used for env variables that are Secret
    secret_name: Optional[str] = None
    # Read secrets from a file in yaml format
    secrets_file: Optional[Path] = None

    # Configure the deployment
    deploy_name: Optional[str] = None
    pod_name: Optional[str] = None
    replicas: int = 1
    pod_node_selector: Optional[Dict[str, str]] = None
    restart_policy: RestartPolicy = RestartPolicy.ALWAYS
    termination_grace_period_seconds: Optional[int] = None

    # Configure the service
    create_service: bool = False
    service_name: Optional[str] = None
    service_type: Optional[ServiceType] = None
    # The port that will be exposed by the service.
    service_port: int = 8080
    # The node_port that will be exposed by the service if service_type = ServiceType.NODE_PORT
    node_port: Optional[int] = None
    # The target_port is the port to access on the pods targeted by the service.
    # It can be the port number or port name on the pod.
    target_port: Optional[Union[str, int]] = None

    # Other args
    load_examples: bool = False
    print_env_on_load: bool = True


class AirflowBase(PhidataApp):
    def __init__(
        self,
        name: str = "airflow",
        version: str = "1",
        enabled: bool = True,
        # Image args,
        image_name: str = "phidata/airflow",
        image_tag: str = "1",
        entrypoint: Optional[Union[str, List]] = None,
        command: Optional[Union[str, List]] = None,
        # Mount the workspace directory on the container,
        mount_workspace: bool = True,
        workspace_volume_name: str = "airflow-ws-volume",
        # Path to mount the workspace volume under,
        # This is the parent directory for the workspace on the container,
        # i.e. the ws is mounted as a subdir in this dir,
        # eg: if ws name is: idata, workspace_dir would be: /usr/local/workspaces/idata,
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
        # Mount aws config on the container,
        # Only on DockerContainers, for K8sContainers use IamRole,
        mount_aws_config: bool = False,
        aws_config_volume_name: str = "airflow-aws-config-volume",
        # Aws config dir on the host,
        aws_config_path: Path = Path.home().resolve().joinpath(".aws"),
        # Aws config dir on the container,
        aws_config_container_path: str = "/root/.aws",
        # Configure airflow,
        # If use_products_as_airflow_dags = True,
        # set the AIRFLOW__CORE__DAGS_FOLDER to the products_dir,
        use_products_as_airflow_dags: bool = True,
        # If use_products_as_airflow_dags = False,
        # set the AIRFLOW__CORE__DAGS_FOLDER to the airflow_dags_path,
        # airflow_dags_path is the directory in the container containing the airflow dags,
        airflow_dags_path: Optional[str] = None,
        # Creates an airflow user with username: test, pass: test,
        create_airflow_test_user: bool = False,
        executor: Literal[
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
        # If init_airflow_db = True, initialize the airflow_db,
        init_airflow_db: bool = False,
        wait_for_db: bool = False,
        # Connect to database using DbApp,
        db_app: Optional[DbApp] = None,
        # Connect to database manually,
        db_user: Optional[str] = None,
        db_password: Optional[str] = None,
        db_schema: Optional[str] = None,
        db_host: Optional[str] = None,
        db_port: Optional[str] = None,
        db_driver: str = "postgresql+psycopg2",
        # Airflow db connections in the format { conn_id: conn_url },
        # converted to env var: AIRFLOW_CONN__conn_id = conn_url,
        db_connections: Optional[Dict] = None,
        # Configure airflow redis,
        wait_for_redis: bool = False,
        # Connect to redis using PhidataApp,
        redis_app: Optional[Any] = None,
        # Connect to redis manually,
        redis_user: Optional[str] = None,
        redis_password: Optional[str] = None,
        redis_schema: Optional[str] = None,
        redis_host: Optional[str] = None,
        redis_port: Optional[str] = None,
        # Configure the container,
        container_name: Optional[str] = None,
        image_pull_policy: ImagePullPolicy = ImagePullPolicy.IF_NOT_PRESENT,
        # Open the container port if create_port=True,
        # Used by the airflow-webserver,
        create_port: bool = False,
        container_port: int = 8080,
        # Only used by the K8sContainer,
        container_port_name: str = "http",
        # Only used by the DockerContainer,
        container_host_port: int = 8080,
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
        # Configure the deployment,
        deploy_name: Optional[str] = None,
        pod_name: Optional[str] = None,
        replicas: int = 1,
        pod_node_selector: Optional[Dict[str, str]] = None,
        restart_policy: RestartPolicy = RestartPolicy.ALWAYS,
        termination_grace_period_seconds: Optional[int] = None,
        # Configure the service,
        create_service: bool = False,
        service_name: Optional[str] = None,
        service_type: Optional[ServiceType] = None,
        # The port that will be exposed by the service.,
        service_port: int = 8080,
        # The node_port that will be exposed by the service if service_type = ServiceType.NODE_PORT,
        node_port: Optional[int] = None,
        # The target_port is the port to access on the pods targeted by the service.,
        # It can be the port number or port name on the pod.,
        target_port: Optional[Union[str, int]] = None,
        # Other args,
        load_examples: bool = False,
        print_env_on_load: bool = True,
        # Additional args
        # If True, skip resource creation if active resources with the same name exist.
        use_cache: bool = True,
        # If True, log extra debug messages
        use_verbose_logs: bool = False,
    ):
        super().__init__()
        try:
            self.args: AirflowBaseArgs = AirflowBaseArgs(
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
                aws_config_volume_name=aws_config_volume_name,
                aws_config_path=aws_config_path,
                aws_config_container_path=aws_config_container_path,
                use_products_as_airflow_dags=use_products_as_airflow_dags,
                airflow_dags_path=airflow_dags_path,
                create_airflow_test_user=create_airflow_test_user,
                executor=executor,
                logging_level=logging_level,
                init_airflow_db=init_airflow_db,
                wait_for_db=wait_for_db,
                db_app=db_app,
                db_user=db_user,
                db_password=db_password,
                db_schema=db_schema,
                db_host=db_host,
                db_port=db_port,
                db_driver=db_driver,
                db_connections=db_connections,
                wait_for_redis=wait_for_redis,
                redis_app=redis_app,
                redis_user=redis_user,
                redis_password=redis_password,
                redis_schema=redis_schema,
                redis_host=redis_host,
                redis_port=redis_port,
                container_name=container_name,
                image_pull_policy=image_pull_policy,
                create_port=create_port,
                container_port=container_port,
                container_port_name=container_port_name,
                container_host_port=container_host_port,
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
                create_service=create_service,
                service_name=service_name,
                service_type=service_type,
                service_port=service_port,
                node_port=node_port,
                target_port=target_port,
                load_examples=load_examples,
                print_env_on_load=print_env_on_load,
                use_cache=use_cache,
                use_verbose_logs=use_verbose_logs,
            )
        except Exception as e:
            logger.error(f"Args for {self.__class__.__name__} are not valid")
            raise

    def get_container_name(self) -> str:
        return self.args.container_name or get_default_container_name(self.args.name)

    def get_service_name(self) -> str:
        return self.args.service_name or get_default_service_name(self.args.name)

    def get_service_port(self) -> int:
        return self.args.service_port

    def get_env_data_from_file(self) -> Optional[Dict[str, str]]:
        env_file_path = self.args.env_file
        if (
            env_file_path is not None
            and env_file_path.exists()
            and env_file_path.is_file()
        ):
            import yaml

            logger.debug(f"Reading {env_file_path}")
            env_data_from_file = yaml.safe_load(env_file_path.read_text())
            if env_data_from_file is not None and isinstance(env_data_from_file, dict):
                return env_data_from_file
            else:
                print_error(f"Invalid env_file: {env_file_path}")
        return None

    def get_secret_data_from_file(self) -> Optional[Dict[str, str]]:
        secrets_file_path = self.args.secrets_file
        if (
            secrets_file_path is not None
            and secrets_file_path.exists()
            and secrets_file_path.is_file()
        ):
            import yaml

            logger.debug(f"Reading {secrets_file_path}")
            secret_data_from_file = yaml.safe_load(secrets_file_path.read_text())
            if secret_data_from_file is not None and isinstance(
                secret_data_from_file, dict
            ):
                return secret_data_from_file
            else:
                print_error(f"Invalid secrets_file: {secrets_file_path}")
        return None

    ######################################################
    ## Docker Resources
    ######################################################

    def get_docker_rg(
        self, docker_build_context: DockerBuildContext
    ) -> Optional[DockerResourceGroup]:

        app_name = self.args.name
        logger.debug(f"Building {app_name} DockerResourceGroup")

        # Workspace paths
        workspace_name = self.workspace_root_path.stem
        workspace_root_container_path = Path(
            self.args.workspace_parent_container_path
        ).joinpath(workspace_name)
        requirements_file_container_path = workspace_root_container_path.joinpath(
            self.args.requirements_file_path
        )
        scripts_dir_container_path = workspace_root_container_path.joinpath(
            self.scripts_dir
        )
        storage_dir_container_path = workspace_root_container_path.joinpath(
            self.storage_dir
        )
        meta_dir_container_path = workspace_root_container_path.joinpath(self.meta_dir)
        products_dir_container_path = workspace_root_container_path.joinpath(
            self.products_dir
        )
        notebooks_dir_container_path = workspace_root_container_path.joinpath(
            self.notebooks_dir
        )
        workspace_config_dir_container_path = workspace_root_container_path.joinpath(
            self.workspace_config_dir
        )

        # Airflow db connection
        db_user = self.args.db_user
        db_password = self.args.db_password
        db_schema = self.args.db_schema
        db_host = self.args.db_host
        db_port = self.args.db_port
        db_driver = self.args.db_driver
        if self.args.db_app is not None and isinstance(self.args.db_app, DbApp):
            logger.debug(
                f"Reading Airflow db connection from DbApp: {self.args.db_app.name}"
            )
            if db_user is None:
                db_user = self.args.db_app.get_db_user()
            if db_password is None:
                db_password = self.args.db_app.get_db_password()
            if db_schema is None:
                db_schema = self.args.db_app.get_db_schema()
            if db_host is None:
                db_host = self.args.db_app.get_db_host_docker()
            if db_port is None:
                db_port = self.args.db_app.get_db_port_docker()
            if db_driver is None:
                db_driver = self.args.db_app.get_db_driver()
        db_connection_url = (
            f"{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_schema}"
        )

        # Container Environment
        container_env: Dict[str, str] = {
            # Env variables used by data workflows and data assets
            "PHI_WORKSPACE_PARENT": str(self.args.workspace_parent_container_path),
            "PHI_WORKSPACE_ROOT": str(workspace_root_container_path),
            "PHI_SCRIPTS_DIR": str(scripts_dir_container_path),
            "PHI_STORAGE_DIR": str(storage_dir_container_path),
            "PHI_META_DIR": str(meta_dir_container_path),
            "PHI_PRODUCTS_DIR": str(products_dir_container_path),
            "PHI_NOTEBOOKS_DIR": str(notebooks_dir_container_path),
            "PHI_WORKSPACE_CONFIG_DIR": str(workspace_config_dir_container_path),
            "INSTALL_REQUIREMENTS": str(self.args.install_requirements),
            "REQUIREMENTS_FILE_PATH": str(requirements_file_container_path),
            "MOUNT_WORKSPACE": str(self.args.mount_workspace),
            # Print env when the container starts
            "PRINT_ENV_ON_LOAD": str(self.args.print_env_on_load),
            # Env variables used by Airflow
            # INIT_AIRFLOW env var is required for phidata to generate DAGs
            "INIT_AIRFLOW": str(True),
            "WAIT_FOR_DB": str(self.args.wait_for_db),
            "INIT_AIRFLOW_DB": str(self.args.init_airflow_db),
            "DB_USER": str(db_user),
            "DB_PASSWORD": str(db_password),
            "DB_SCHEMA": str(db_schema),
            "DB_HOST": str(db_host),
            "DB_PORT": str(db_port),
            "WAIT_FOR_REDIS": str(self.args.wait_for_redis),
            "REDIS_USER": str(self.args.redis_user),
            "REDIS_PASSWORD": str(self.args.redis_password),
            "REDIS_SCHEMA": str(self.args.redis_schema),
            "REDIS_HOST": str(self.args.redis_host),
            "REDIS_PORT": str(self.args.redis_port),
            "AIRFLOW__CORE__LOAD_EXAMPLES": str(self.args.load_examples),
            "CREATE_AIRFLOW_TEST_USER": str(self.args.create_airflow_test_user),
            "AIRFLOW__CORE__EXECUTOR": str(self.args.executor),
            "AIRFLOW__LOGGING__LOGGING_LEVEL": str(self.args.logging_level),
            # "AIRFLOW__CELERY__RESULT_BACKEND": f"db+{self.args.pg_driver}://{self.args.pg_user}:{self.args.pg_password}@{self.args.pg_container_name}:{self.args.pg_container_port}/{self.args.pg_schema}{self.args.pg_extras}",
            # "AIRFLOW__CELERY__BROKER_URL": f"{self.args.redis_driver}://{self.args.redis_pass}@{self.args.redis_container_name}/{self.args.redis_schema}",
            # "AIRFLOW__CORE__FERNET_KEY": "FpErWX7ZxRBGxuAq2JDfle3A7k7Xxi5hY0wh_u0X0Go=",
            # "AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION": "True",
        }
        # Set the AIRFLOW__CORE__SQL_ALCHEMY_CONN
        if "None" not in db_connection_url:
            container_env["AIRFLOW__CORE__SQL_ALCHEMY_CONN"] = db_connection_url
        # Set the AIRFLOW__CORE__DAGS_FOLDER
        if self.args.mount_workspace and self.args.use_products_as_airflow_dags:
            container_env["AIRFLOW__CORE__DAGS_FOLDER"] = str(
                products_dir_container_path
            )
        elif self.args.airflow_dags_path is not None:
            container_env["AIRFLOW__CORE__DAGS_FOLDER"] = self.args.airflow_dags_path
        # Set the AIRFLOW__CONN_ variables
        if self.args.db_connections is not None:
            for conn_id, conn_url in self.args.db_connections.items():
                try:
                    af_conn_id = str("AIRFLOW_CONN_{}".format(conn_id)).upper()
                    container_env[af_conn_id] = conn_url
                except Exception as e:
                    logger.exception(e)
                    continue
        # Update the container env using env_file
        env_data_from_file = self.get_env_data_from_file()
        if env_data_from_file is not None:
            container_env.update(env_data_from_file)
        # Update the container env with user provided env
        if self.args.env is not None and isinstance(self.args.env, dict):
            container_env.update(self.args.env)

        # Container Volumes
        # container_volumes is a dictionary which configures the volumes to mount
        # inside the container. The key is either the host path or a volume name,
        # and the value is a dictionary with 2 keys:
        #   bind - The path to mount the volume inside the container
        #   mode - Either rw to mount the volume read/write, or ro to mount it read-only.
        # For example:
        # {
        #   '/home/user1/': {'bind': '/mnt/vol2', 'mode': 'rw'},
        #   '/var/www': {'bind': '/mnt/vol1', 'mode': 'ro'}
        # }
        container_volumes = {}
        # Create a volume for the workspace dir
        if self.args.mount_workspace:
            workspace_root_path_str = str(self.workspace_root_path)
            workspace_root_container_path_str = str(workspace_root_container_path)
            logger.debug(f"Mounting: {workspace_root_path_str}")
            logger.debug(f"\tto: {workspace_root_container_path_str}")
            container_volumes[workspace_root_path_str] = {
                "bind": workspace_root_container_path_str,
                "mode": "rw",
            }
        # Create a volume for aws config
        if self.args.mount_aws_config:
            aws_config_path_str = str(self.args.aws_config_path)
            logger.debug(f"Mounting: {aws_config_path_str}")
            logger.debug(f"\tto: {self.args.aws_config_container_path}")
            container_volumes[aws_config_path_str] = {
                "bind": self.args.aws_config_container_path,
                "mode": "ro",
            }
            container_env[
                "AWS_CONFIG_FILE"
            ] = f"{self.args.aws_config_container_path}/config"
            container_env[
                "AWS_SHARED_CREDENTIALS_FILE"
            ] = f"{self.args.aws_config_container_path}/credentials"

        # Container Ports
        # container_ports is a dictionary which configures the ports to bind
        # inside the container. The key is the port to bind inside the container
        #   either as an integer or a string in the form port/protocol
        # and the value is the corresponding port to open on the host.
        # For example:
        #   {'2222/tcp': 3333} will expose port 2222 inside the container as port 3333 on the host.
        container_ports: Dict[str, int] = {}
        if self.args.create_port:
            container_ports[
                str(self.args.container_port)
            ] = self.args.container_host_port

        # Create the container
        docker_container = DockerContainer(
            name=self.get_container_name(),
            image=get_image_str(self.args.image_name, self.args.image_tag),
            entrypoint=self.args.entrypoint,
            command=self.args.command,
            detach=self.args.container_detach,
            auto_remove=self.args.container_auto_remove,
            remove=self.args.container_remove,
            stdin_open=True,
            tty=True,
            environment=container_env,
            network=docker_build_context.network,
            ports=container_ports if len(container_ports) > 0 else None,
            volumes=container_volumes,
            use_cache=self.args.use_cache,
            use_verbose_logs=self.args.use_verbose_logs,
        )
        # logger.debug(f"Container Env: {docker_container.environment}")

        docker_rg = DockerResourceGroup(
            name=app_name,
            enabled=self.args.enabled,
            network=DockerNetwork(name=docker_build_context.network),
            containers=[docker_container],
        )
        return docker_rg

    def init_docker_resource_groups(
        self, docker_build_context: DockerBuildContext
    ) -> None:
        docker_rg = self.get_docker_rg(docker_build_context)
        if docker_rg is not None:
            if self.docker_resource_groups is None:
                self.docker_resource_groups = OrderedDict()
            self.docker_resource_groups[docker_rg.name] = docker_rg

    ######################################################
    ## K8s Resources
    ######################################################

    def get_k8s_rg(
        self, k8s_build_context: K8sBuildContext
    ) -> Optional[K8sResourceGroup]:

        app_name = self.args.name
        logger.debug(f"Building {app_name} K8sResourceGroup")

        # Define K8s resources
        config_maps: List[CreateConfigMap] = []
        secrets: List[CreateSecret] = []
        volumes: List[CreateVolume] = []
        containers: List[CreateContainer] = []

        # Workspace paths
        workspace_name = self.workspace_root_path.stem
        workspace_root_container_path = Path(
            self.args.workspace_parent_container_path
        ).joinpath(workspace_name)
        requirements_file_container_path = workspace_root_container_path.joinpath(
            self.args.requirements_file_path
        )
        scripts_dir_container_path = workspace_root_container_path.joinpath(
            self.scripts_dir
        )
        storage_dir_container_path = workspace_root_container_path.joinpath(
            self.storage_dir
        )
        meta_dir_container_path = workspace_root_container_path.joinpath(self.meta_dir)
        products_dir_container_path = workspace_root_container_path.joinpath(
            self.products_dir
        )
        notebooks_dir_container_path = workspace_root_container_path.joinpath(
            self.notebooks_dir
        )
        workspace_config_dir_container_path = workspace_root_container_path.joinpath(
            self.workspace_config_dir
        )

        # Airflow db connection
        db_user = self.args.db_user
        db_password = self.args.db_password
        db_schema = self.args.db_schema
        db_host = self.args.db_host
        db_port = self.args.db_port
        db_driver = self.args.db_driver
        if self.args.db_app is not None and isinstance(self.args.db_app, DbApp):
            logger.debug(
                f"Reading Airflow db connection from DbApp: {self.args.db_app.name}"
            )
            if db_user is None:
                db_user = self.args.db_app.get_db_user()
            if db_password is None:
                db_password = self.args.db_app.get_db_password()
            if db_schema is None:
                db_schema = self.args.db_app.get_db_schema()
            if db_host is None:
                db_host = self.args.db_app.get_db_host_k8s()
            if db_port is None:
                db_port = self.args.db_app.get_db_port_k8s()
            if db_driver is None:
                db_driver = self.args.db_app.get_db_driver()
        db_connection_url = (
            f"{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_schema}"
        )

        # Container Environment
        container_env: Dict[str, str] = {
            # Env variables used by data workflows and data assets
            "PHI_WORKSPACE_PARENT": str(self.args.workspace_parent_container_path),
            "PHI_WORKSPACE_ROOT": str(workspace_root_container_path),
            "PHI_SCRIPTS_DIR": str(scripts_dir_container_path),
            "PHI_STORAGE_DIR": str(storage_dir_container_path),
            "PHI_META_DIR": str(meta_dir_container_path),
            "PHI_PRODUCTS_DIR": str(products_dir_container_path),
            "PHI_NOTEBOOKS_DIR": str(notebooks_dir_container_path),
            "PHI_WORKSPACE_CONFIG_DIR": str(workspace_config_dir_container_path),
            "INSTALL_REQUIREMENTS": str(self.args.install_requirements),
            "REQUIREMENTS_FILE_PATH": str(requirements_file_container_path),
            "MOUNT_WORKSPACE": str(self.args.mount_workspace),
            # Print env when the container starts
            "PRINT_ENV_ON_LOAD": str(self.args.print_env_on_load),
            # Env variables used by Airflow
            # INIT_AIRFLOW env var is required for phidata to create DAGs
            "INIT_AIRFLOW": str(True),
            "WAIT_FOR_DB": str(self.args.wait_for_db),
            "INIT_AIRFLOW_DB": str(self.args.init_airflow_db),
            "DB_USER": str(db_user),
            "DB_PASSWORD": str(db_password),
            "DB_SCHEMA": str(db_schema),
            "DB_HOST": str(db_host),
            "DB_PORT": str(db_port),
            "WAIT_FOR_REDIS": str(self.args.wait_for_redis),
            "REDIS_USER": str(self.args.redis_user),
            "REDIS_PASSWORD": str(self.args.redis_password),
            "REDIS_SCHEMA": str(self.args.redis_schema),
            "REDIS_HOST": str(self.args.redis_host),
            "REDIS_PORT": str(self.args.redis_port),
            "AIRFLOW__CORE__LOAD_EXAMPLES": str(self.args.load_examples),
            "CREATE_AIRFLOW_TEST_USER": str(self.args.create_airflow_test_user),
            "AIRFLOW__CORE__EXECUTOR": str(self.args.executor),
            "AIRFLOW__LOGGING__LOGGING_LEVEL": str(self.args.logging_level),
            # "AIRFLOW__CELERY__RESULT_BACKEND": f"db+{self.args.pg_driver}://{self.args.pg_user}:{self.args.pg_password}@{self.args.pg_container_name}:{self.args.pg_container_port}/{self.args.pg_schema}{self.args.pg_extras}",
            # "AIRFLOW__CELERY__BROKER_URL": f"{self.args.redis_driver}://{self.args.redis_pass}@{self.args.redis_container_name}/{self.args.redis_schema}",
            # "AIRFLOW__CORE__FERNET_KEY": "FpErWX7ZxRBGxuAq2JDfle3A7k7Xxi5hY0wh_u0X0Go=",
            # "AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION": "True",
        }
        # Set the AIRFLOW__CORE__SQL_ALCHEMY_CONN
        if "None" not in db_connection_url:
            logger.debug(f"AIRFLOW__CORE__SQL_ALCHEMY_CONN: {db_connection_url}")
            container_env["AIRFLOW__CORE__SQL_ALCHEMY_CONN"] = db_connection_url
        # Set the AIRFLOW__CORE__DAGS_FOLDER
        if self.args.mount_workspace and self.args.use_products_as_airflow_dags:
            container_env["AIRFLOW__CORE__DAGS_FOLDER"] = str(
                products_dir_container_path
            )
        elif self.args.airflow_dags_path is not None:
            container_env["AIRFLOW__CORE__DAGS_FOLDER"] = self.args.airflow_dags_path
        # Set the AIRFLOW__CONN_ variables
        if self.args.db_connections is not None:
            for conn_id, conn_url in self.args.db_connections.items():
                try:
                    af_conn_id = str("AIRFLOW_CONN_{}".format(conn_id)).upper()
                    container_env[af_conn_id] = conn_url
                except Exception as e:
                    logger.exception(e)
                    continue
        # Update the container env using env_file
        env_data_from_file = self.get_env_data_from_file()
        if env_data_from_file is not None:
            container_env.update(env_data_from_file)
        # Update the container env with user provided env
        if self.args.env is not None and isinstance(self.args.env, dict):
            container_env.update(self.args.env)

        # Create a ConfigMap to set the container env variables which are not Secret
        container_env_cm = CreateConfigMap(
            cm_name=self.args.config_map_name or get_default_configmap_name(app_name),
            app_name=app_name,
            data=container_env,
        )
        config_maps.append(container_env_cm)

        # Create a Secret to set the container env variables which are Secret
        secret_data_from_file = self.get_secret_data_from_file()
        if secret_data_from_file is not None:
            container_env_secret = CreateSecret(
                secret_name=self.args.secret_name or get_default_secret_name(app_name),
                app_name=app_name,
                data=secret_data_from_file,
            )
            secrets.append(container_env_secret)

        # If mount_workspace=True
        # Create a Sidecar git-sync container and volume
        if self.args.mount_workspace:
            workspace_parent_container_path_str = str(
                self.args.workspace_parent_container_path
            )
            logger.debug(f"Creating EmptyDir")
            logger.debug(f"\tat: {workspace_parent_container_path_str}")
            workspace_volume = CreateVolume(
                volume_name=self.args.workspace_volume_name,
                app_name=app_name,
                mount_path=workspace_parent_container_path_str,
                volume_type=VolumeType.EMPTY_DIR,
            )
            volumes.append(workspace_volume)
            if self.args.create_git_sync_sidecar:
                if self.args.git_sync_repo is None:
                    print_error("git_sync_repo invalid")
                else:
                    git_sync_env = {
                        "GIT_SYNC_REPO": self.args.git_sync_repo,
                        "GIT_SYNC_ROOT": str(self.args.workspace_parent_container_path),
                        "GIT_SYNC_DEST": workspace_name,
                    }
                    if self.args.git_sync_branch is not None:
                        git_sync_env["GIT_SYNC_BRANCH"] = self.args.git_sync_branch
                    if self.args.git_sync_wait is not None:
                        git_sync_env["GIT_SYNC_WAIT"] = str(self.args.git_sync_wait)
                    git_sync_sidecar = CreateContainer(
                        container_name="git-sync-workspaces",
                        app_name=app_name,
                        image_name="k8s.gcr.io/git-sync",
                        image_tag="v3.1.1",
                        env=git_sync_env,
                        volumes=[workspace_volume],
                    )
                    containers.append(git_sync_sidecar)

        # Create the ports to open
        container_port: Optional[CreatePort] = None
        if self.args.create_port:
            container_port = CreatePort(
                name=self.args.container_port_name,
                container_port=self.args.container_port,
                service_port=self.args.service_port,
                target_port=self.args.target_port or self.args.container_port_name,
            )

        # Create the container
        k8s_container = CreateContainer(
            container_name=self.get_container_name(),
            app_name=app_name,
            image_name=self.args.image_name,
            image_tag=self.args.image_tag,
            # Equivalent to docker images CMD
            args=[self.args.command]
            if isinstance(self.args.command, str)
            else self.args.command,
            # Equivalent to docker images ENTRYPOINT
            command=self.args.entrypoint,
            image_pull_policy=self.args.image_pull_policy,
            envs_from_configmap=[cm.cm_name for cm in config_maps]
            if len(config_maps) > 0
            else None,
            envs_from_secret=[secret.secret_name for secret in secrets]
            if len(secrets) > 0
            else None,
            ports=[container_port] if container_port is not None else None,
            volumes=volumes if len(volumes) > 0 else None,
            labels=k8s_build_context.labels,
        )
        containers.append(k8s_container)

        # Create the deployment
        k8s_deployment = CreateDeployment(
            deploy_name=self.args.deploy_name or get_default_deploy_name(app_name),
            pod_name=self.args.pod_name or get_default_pod_name(app_name),
            app_name=app_name,
            namespace=k8s_build_context.namespace,
            service_account_name=k8s_build_context.service_account_name,
            replicas=self.args.replicas,
            containers=containers if len(containers) > 0 else None,
            pod_node_selector=self.args.pod_node_selector,
            restart_policy=self.args.restart_policy,
            termination_grace_period_seconds=self.args.termination_grace_period_seconds,
            volumes=volumes if len(volumes) > 0 else None,
            labels=k8s_build_context.labels,
        )

        # Create the service
        k8s_service: Optional[CreateService] = None
        if self.args.create_service:
            k8s_service = CreateService(
                service_name=self.get_service_name(),
                app_name=app_name,
                namespace=k8s_build_context.namespace,
                service_account_name=k8s_build_context.service_account_name,
                service_type=self.args.service_type,
                deployment=k8s_deployment,
                ports=[container_port] if container_port is not None else None,
                labels=k8s_build_context.labels,
            )

        # Create the K8sResourceGroup
        k8s_resource_group = CreateK8sResourceGroup(
            name=app_name,
            enabled=self.args.enabled,
            config_maps=config_maps if len(config_maps) > 0 else None,
            secrets=secrets if len(secrets) > 0 else None,
            services=[k8s_service] if k8s_service is not None else None,
            deployments=[k8s_deployment],
        )

        return k8s_resource_group.create()

    def init_k8s_resource_groups(self, k8s_build_context: K8sBuildContext) -> None:
        k8s_rg = self.get_k8s_rg(k8s_build_context)
        if k8s_rg is not None:
            if self.k8s_resource_groups is None:
                self.k8s_resource_groups = OrderedDict()
            self.k8s_resource_groups[k8s_rg.name] = k8s_rg
