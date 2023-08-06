from collections import OrderedDict
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from typing_extensions import Literal

from phidata.app import PhidataApp, PhidataAppArgs
from phidata.infra.docker.resource.network import DockerNetwork
from phidata.infra.docker.resource.container import DockerContainer
from phidata.infra.docker.resource.group import (
    DockerResourceGroup,
    DockerBuildContext,
)
from phidata.infra.k8s.create.apps.v1.deployment import CreateDeployment
from phidata.infra.k8s.create.core.v1.secret import CreateSecret
from phidata.infra.k8s.create.core.v1.config_map import CreateConfigMap
from phidata.infra.k8s.create.core.v1.container import CreateContainer
from phidata.infra.k8s.create.core.v1.volume import (
    CreateVolume,
    EmptyDirVolumeSource,
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
    get_default_volume_name,
    get_default_deploy_name,
    get_default_pod_name,
)
from phidata.utils.cli_console import print_error
from phidata.utils.log import logger


class AirflowArgs(PhidataAppArgs):
    name: str = "airflow"
    version: str = "1"
    enabled: bool = True

    # Webserver Args
    ws_enabled: bool = True
    ws_image_name: str = "phidata/airflow"
    ws_image_tag: str = "1"
    ws_entrypoint: str = "/entrypoint.sh"
    ws_command: str = "webserver"
    ws_env: Optional[Dict[str, str]] = None
    # Set as True to init the airflow db before running the webserver
    ws_init_airflow_db: bool = False
    # Set as True to wait for the airflow db to be available before running the webserver
    ws_wait_for_db: bool = False
    # Set as True to wait for redis to be available before running the webserver
    ws_wait_for_redis: bool = False
    # Webserver Docker Args
    ws_container_name: str = "airflow-ws"
    ws_container_port: str = "8080"
    ws_container_host_port: int = 8080
    # Webserver K8s Args
    # ws_rg_name: str = "airflow-webserver"
    # ws_svc_name: str = "airflow-webserver-svc"
    # ws_deploy_name: str = "airflow-webserver-deploy"
    # ws_replicas: int = 1
    # ws_port_name: str = "http"
    # ws_port_number: int = 8080

    # Scheduler Args
    scheduler_enabled: bool = True
    scheduler_image_name: str = "phidata/airflow"
    scheduler_image_tag: str = "0.1"
    scheduler_entrypoint: str = "/entrypoint.sh"
    scheduler_command: str = "scheduler"
    scheduler_env: Optional[Dict[str, str]] = None
    scheduler_init_airflow_db: bool = False
    scheduler_wait_for_db: bool = False
    scheduler_wait_for_redis: bool = False
    scheduler_container_name: str = "airflow-scheduler"

    # Worker Args
    worker_enabled: bool = True
    worker_image_name: str = "phidata/airflow"
    worker_image_tag: str = "0.1"
    worker_entrypoint: str = "/entrypoint.sh"
    worker_command: str = "worker"
    worker_env: Optional[Dict[str, str]] = None
    worker_container_name: str = "airflow-worker"

    # Flower Args
    flower_enabled: bool = True
    flower_image_name: str = "phidata/airflow"
    flower_image_tag: str = "0.1"
    flower_entrypoint: str = "/entrypoint.sh"
    flower_command: str = "flower"
    flower_env: Optional[Dict[str, str]] = None
    flower_container_name: str = "airflow-flower"
    flower_container_port: str = "5555"
    flower_container_host_port: int = 5555

    # DB Args
    db_enabled: bool = True
    db_type: Literal["postgres", "mysql"] = "postgres"
    # Postgres as DB args
    pg_image_name: str = "postgres"
    pg_image_tag: str = "13"
    pg_driver: str = "postgresql"
    pg_env: Optional[Dict[str, str]] = None
    pg_user: str = "airflow"
    pg_password: str = "airflow"
    pg_schema: str = "airflow"
    pg_extras: str = ""
    pg_data_path: str = "/var/lib/postgresql/data/"
    # Postgres Docker Args
    pg_container_name: str = "airflow-pg"
    pg_container_port: str = "5432"
    pg_container_host_port: int = 5432
    # We currently let docker manage the storage of our database data
    pg_volume_name: str = "airflow_pg_data"
    # The directory on the users (host) machine containing the postgres data files
    # pg_data_host_path: Optional[str] = None
    # K8s Args
    # pg_rg_name: str = "airflow-pg"
    # pg_svc_name: str = "airflow-pg-svc"
    # pg_deploy_name: str = "airflow-pg-deploy"
    # pg_replicas: int = 1
    # pg_pvc_name: str = "airflow-pg-pvc"
    # pg_cm_name: str = "airflow-pg-cm"

    # Redis Args
    redis_enabled: bool = True
    redis_image_name: str = "redis"
    redis_image_tag: str = "latest"
    redis_driver: str = "redis"
    redis_user: str = "airflow"
    redis_pass: str = "airflow"
    redis_schema: str = "1"
    # Redis Docker Args
    redis_container_name: str = "airflow-redis"
    redis_container_port: str = "6379"
    redis_container_host_port: int = 6379
    # K8s Args
    # redis_svc_name: str = "airflow-redis-svc"
    # redis_deploy_name: str = "airflow-redis-deploy"

    # Common Args
    # The directory on the users (host) machine containing the airflow DAG files, starting from the workspace_root_path.
    airflow_dags_host_dir_path: str = "/projects"
    # The path on the users (host) machine for the dir of airflow.cfg file, starting from the workspace_root_path.
    airflow_conf_host_dir_path: str = "/workspace/airflow"
    # The directory in the container containing the airflow pipelines
    airflow__core__dags_folder: str = "/usr/local/airflow/dags"
    # The path in the container for the airflow.cfg file
    airflow__core__conf_dir: str = "/usr/local/airflow"

    # Common K8s Args
    # cm_name: str = "airflow-cm"
    # Storage Classes
    # ssd_rg_name: str = "airflow-ssd"
    # ssd_storage_class_name: str = "airflow-ssd"


class Airflow(PhidataApp):
    def __init__(
        self,
        name: str = "airflow",
        version: str = "1",
        enabled: bool = True,
        ws_enabled: bool = False,
        ws_image_name: str = "phidata/airflow",
        ws_image_tag: str = "0.5",
        ws_entrypoint: str = "/entrypoint.sh",
        ws_command: str = "webserver",
        ws_env: Optional[Dict[str, str]] = None,
        ws_init_airflow_db: bool = False,
        ws_wait_for_db: bool = True,
        ws_wait_for_redis: bool = True,
        ws_container_name: str = "airflow-ws",
        ws_container_port: str = "8080",
        ws_container_host_port: int = 9090,
        scheduler_enabled: bool = False,
        scheduler_image_name: str = "phidata/airflow",
        scheduler_image_tag: str = "0.5",
        scheduler_entrypoint: str = "/entrypoint.sh",
        scheduler_command: str = "scheduler",
        scheduler_env: Optional[Dict[str, str]] = None,
        scheduler_init_airflow_db: bool = True,
        scheduler_wait_for_db: bool = True,
        scheduler_wait_for_redis: bool = True,
        scheduler_container_name: str = "airflow-scheduler",
        worker_enabled: bool = False,
        worker_image_name: str = "phidata/airflow",
        worker_image_tag: str = "0.1",
        worker_entrypoint: str = "/entrypoint.sh",
        worker_command: str = "worker",
        worker_env: Optional[Dict[str, str]] = None,
        worker_container_name: str = "airflow-worker",
        flower_enabled: bool = False,
        flower_image_name: str = "phidata/airflow",
        flower_image_tag: str = "0.1",
        flower_entrypoint: str = "/entrypoint.sh",
        flower_command: str = "flower",
        flower_env: Optional[Dict[str, str]] = None,
        flower_container_name: str = "airflow-flower",
        flower_container_port: str = "5555",
        flower_container_host_port: int = 6000,
        db_enabled: bool = False,
        db_type: Literal["postgres", "mysql"] = "postgres",
        pg_image_name: str = "postgres",
        pg_image_tag: str = "13",
        pg_driver: str = "postgresql",
        pg_env: Optional[Dict[str, str]] = None,
        pg_user: str = "airflow",
        pg_password: str = "airflow",
        pg_schema: str = "airflow",
        pg_data_path: str = "/var/lib/postgresql/data/",
        pg_container_name: str = "airflow-pg",
        pg_container_port: str = "5432",
        pg_container_host_port: int = 5500,
        pg_volume_name: str = "airflow_pg_data",
        redis_enabled: bool = False,
        redis_image_name: str = "redis",
        redis_image_tag: str = "latest",
        redis_driver: str = "redis",
        redis_user: str = "airflow",
        redis_pass: str = "airflow",
        redis_schema: str = "1",
        redis_container_name: str = "airflow-redis",
        redis_container_port: str = "6379",
        redis_container_host_port: int = 6500,
        airflow_dags_host_dir_path: str = "/projects",
        airflow_conf_host_dir_path: str = "/workspace/airflow",
        airflow__core__dags_folder: str = "/usr/local/airflow/dags",
        airflow__core__conf_dir: str = "/usr/local/airflow",
    ):

        super().__init__()
        try:
            self.args: AirflowArgs = AirflowArgs(
                name=name,
                version=version,
                enabled=enabled,
                ws_enabled=ws_enabled,
                ws_image_name=ws_image_name,
                ws_image_tag=ws_image_tag,
                ws_entrypoint=ws_entrypoint,
                ws_command=ws_command,
                ws_env=ws_env,
                ws_init_airflow_db=ws_init_airflow_db,
                ws_wait_for_db=ws_wait_for_db,
                ws_wait_for_redis=ws_wait_for_redis,
                ws_container_name=ws_container_name,
                ws_container_port=ws_container_port,
                ws_container_host_port=ws_container_host_port,
                scheduler_enabled=scheduler_enabled,
                scheduler_image_name=scheduler_image_name,
                scheduler_image_tag=scheduler_image_tag,
                scheduler_entrypoint=scheduler_entrypoint,
                scheduler_command=scheduler_command,
                scheduler_env=scheduler_env,
                scheduler_init_airflow_db=scheduler_init_airflow_db,
                scheduler_wait_for_db=scheduler_wait_for_db,
                scheduler_wait_for_redis=scheduler_wait_for_redis,
                scheduler_container_name=scheduler_container_name,
                worker_enabled=worker_enabled,
                worker_image_name=worker_image_name,
                worker_image_tag=worker_image_tag,
                worker_entrypoint=worker_entrypoint,
                worker_command=worker_command,
                worker_env=worker_env,
                worker_container_name=worker_container_name,
                flower_enabled=flower_enabled,
                flower_image_name=flower_image_name,
                flower_image_tag=flower_image_tag,
                flower_entrypoint=flower_entrypoint,
                flower_command=flower_command,
                flower_env=flower_env,
                flower_container_name=flower_container_name,
                flower_container_port=flower_container_port,
                flower_container_host_port=flower_container_host_port,
                db_enabled=db_enabled,
                db_type=db_type,
                pg_image_name=pg_image_name,
                pg_image_tag=pg_image_tag,
                pg_driver=pg_driver,
                pg_env=pg_env,
                pg_user=pg_user,
                pg_password=pg_password,
                pg_schema=pg_schema,
                pg_data_path=pg_data_path,
                pg_container_name=pg_container_name,
                pg_container_port=pg_container_port,
                pg_container_host_port=pg_container_host_port,
                pg_volume_name=pg_volume_name,
                redis_enabled=redis_enabled,
                redis_image_name=redis_image_name,
                redis_image_tag=redis_image_tag,
                redis_driver=redis_driver,
                redis_user=redis_user,
                redis_pass=redis_pass,
                redis_schema=redis_schema,
                redis_container_name=redis_container_name,
                redis_container_port=redis_container_port,
                redis_container_host_port=redis_container_host_port,
                airflow_dags_host_dir_path=airflow_dags_host_dir_path,
                airflow_conf_host_dir_path=airflow_conf_host_dir_path,
                airflow__core__dags_folder=airflow__core__dags_folder,
                airflow__core__conf_dir=airflow__core__conf_dir,
            )
        except Exception as e:
            # from phidata.utils.cli_console import print_validation_errors
            #
            # print_validation_errors(e.args)
            raise

        # # these variables can now be accessed using the object instance
        # # Assign the values from self.args so pydantic handles type conversion
        # self.name: str = self.args.name
        # self.version: str = self.args.version
        # self.enabled: bool = self.args.enabled
        # self.ws_enabled: bool = self.args.ws_enabled
        # self.ws_image_name: str = self.args.ws_image_name
        # self.ws_image_tag: str = self.args.ws_image_tag
        # self.ws_entrypoint: str = self.args.ws_entrypoint
        # self.ws_command: str = self.args.ws_command
        # self.ws_env: Optional[Dict[str, str]] = self.args.ws_env
        # self.ws_init_airflow_db: bool = self.args.ws_init_airflow_db
        # self.ws_wait_for_db: bool = self.args.ws_wait_for_db
        # self.ws_wait_for_redis: bool = self.args.ws_wait_for_redis
        # self.ws_container_name: str = self.args.ws_container_name
        # self.ws_container_port: str = self.args.ws_container_port
        # self.ws_container_host_port: int = self.args.ws_container_host_port
        # self.scheduler_enabled: bool = self.args.scheduler_enabled
        # self.scheduler_image_name: str = self.args.scheduler_image_name
        # self.scheduler_image_tag: str = self.args.scheduler_image_tag
        # self.scheduler_entrypoint: str = self.args.scheduler_entrypoint
        # self.scheduler_command: str = self.args.scheduler_command
        # self.scheduler_env: Optional[Dict[str, str]] = self.args.scheduler_env
        # self.scheduler_init_airflow_db: bool = self.args.scheduler_init_airflow_db
        # self.scheduler_wait_for_db: bool = self.args.scheduler_wait_for_db
        # self.scheduler_wait_for_redis: bool = self.args.scheduler_wait_for_redis
        # self.scheduler_container_name: str = self.args.scheduler_container_name
        # self.worker_enabled: bool = self.args.worker_enabled
        # self.worker_image_name: str = self.args.worker_image_name
        # self.worker_image_tag: str = self.args.worker_image_tag
        # self.worker_entrypoint: str = self.args.worker_entrypoint
        # self.worker_command: str = self.args.worker_command
        # self.worker_env: Optional[Dict[str, str]] = self.args.worker_env
        # self.worker_container_name: str = self.args.worker_container_name
        # self.flower_enabled: bool = self.args.flower_enabled
        # self.flower_image_name: str = self.args.flower_image_name
        # self.flower_image_tag: str = self.args.flower_image_tag
        # self.flower_entrypoint: str = self.args.flower_entrypoint
        # self.flower_command: str = self.args.flower_command
        # self.flower_env: Optional[Dict[str, str]] = self.args.flower_env
        # self.flower_container_name: str = self.args.flower_container_name
        # self.flower_container_port: str = self.args.flower_container_port
        # self.flower_container_host_port: int = self.args.flower_container_host_port
        # self.db_enabled: bool = self.args.db_enabled
        # self.db_type: Literal["postgres", "mysql"] = self.args.db_type
        # self.pg_image_name: str = self.args.pg_image_name
        # self.pg_image_tag: str = self.args.pg_image_tag
        # self.pg_driver: str = self.args.pg_driver
        # self.pg_env: Optional[Dict[str, str]] = self.args.pg_env
        # self.pg_user: str = self.args.pg_user
        # self.pg_password: str = self.args.pg_password
        # self.pg_schema: str = self.args.pg_schema
        # self.pg_data_path: str = self.args.pg_data_path
        # self.pg_container_name: str = self.args.pg_container_name
        # self.pg_container_port: str = self.args.pg_container_port
        # self.pg_container_host_port: int = self.args.pg_container_host_port
        # self.pg_volume_name: str = self.args.pg_volume_name
        # self.redis_enabled: bool = self.args.redis_enabled
        # self.redis_image_name: str = self.args.redis_image_name
        # self.redis_image_tag: str = self.args.redis_image_tag
        # self.redis_driver: str = self.args.redis_driver
        # self.redis_user: str = self.args.redis_user
        # self.redis_pass: str = self.args.redis_pass
        # self.redis_schema: str = self.args.redis_schema
        # self.redis_container_name: str = self.args.redis_container_name
        # self.redis_container_port: str = self.args.redis_container_port
        # self.redis_container_host_port: int = self.args.redis_container_host_port
        # self.airflow_dags_host_dir_path: str = self.args.airflow_dags_host_dir_path
        # self.airflow_conf_host_dir_path: str = self.args.airflow_conf_host_dir_path
        # self.airflow__core__dags_folder: str = self.args.airflow__core__dags_folder
        # self.airflow__core__conf_dir: str = self.args.airflow__core__conf_dir

    def get_postgres_docker_rg(
        self, docker_build_context: DockerBuildContext
    ) -> Optional[DockerResourceGroup]:
        logger.debug(f"Init Postgres DockerResourceGroup")

        _postgres_container_env = {
            "POSTGRES_USER": self.args.pg_user,
            "POSTGRES_PASSWORD": self.args.pg_password,
            "POSTGRES_DB": self.args.pg_schema,
            "PGDATA": self.args.pg_data_path,
        }
        if self.args.pg_env is not None and isinstance(self.args.pg_env, dict):
            _postgres_container_env.update(self.args.pg_env)

        _postgres_container = DockerContainer(
            name=self.args.pg_container_name,
            image="{}:{}".format(self.args.pg_image_name, self.args.pg_image_tag),
            detach=True,
            auto_remove=True,
            remove=True,
            network=docker_build_context.network,
            ports={
                self.args.pg_container_port: self.args.pg_container_host_port,
            },
            volumes={
                self.args.pg_volume_name: {
                    "bind": self.args.pg_data_path,
                    "mode": "rw",
                },
            },
        )

        _postgres_rg = DockerResourceGroup(
            name=self.args.pg_container_name,
            enabled=self.args.db_enabled,
            weight=101,
            containers=[_postgres_container],
        )
        # logger.debug("postgres rg:\n{}".format(_postgres_rg.json(indent=2)))
        return _postgres_rg

    def get_redis_docker_rg(
        self, docker_build_context: DockerBuildContext
    ) -> Optional[DockerResourceGroup]:
        logger.debug(f"Init Redis DockerResourceGroup")

        _redis_container = DockerContainer(
            name=self.args.redis_container_name,
            image="{}:{}".format(self.args.redis_image_name, self.args.redis_image_tag),
            detach=True,
            auto_remove=True,
            remove=True,
            network=docker_build_context.network,
            ports={
                self.args.redis_container_port: self.args.redis_container_host_port,
            },
        )

        _redis_rg = DockerResourceGroup(
            name=self.args.redis_container_name,
            enabled=self.args.redis_enabled,
            weight=101,
            containers=[_redis_container],
        )
        # logger.debug("redis rg:\n{}".format(_redis_rg.json(indent=2)))
        return _redis_rg

    def get_scheduler_docker_rg(
        self,
        docker_build_context: DockerBuildContext,
    ) -> Optional[DockerResourceGroup]:
        logger.debug(f"Init Scheduler DockerResourceGroup")

        _airflow_dags_host_dir_path_str = (
            str(self.args.workspace_dir_path) + self.args.airflow_dags_host_dir_path
        )
        _airflow_conf_host_dir_path = (
            str(self.args.workspace_dir_path) + self.args.airflow_conf_host_dir_path
        )
        _scheduler_container_env = {
            "INIT_AIRFLOW_DB": self.args.scheduler_init_airflow_db,
            "WAIT_FOR_DB": self.args.scheduler_wait_for_db,
            "WAIT_FOR_REDIS": self.args.scheduler_wait_for_redis,
            "AIRFLOW_DB_CONN_URL": self.args.pg_container_name,
            "AIRFLOW_DB_CONN_PORT": self.args.pg_container_port,
            "AIRFLOW_DB_USER": self.args.pg_user,
            "AIRFLOW_DB_PASSWORD": self.args.pg_password,
            "AIRFLOW_SCHEMA": self.args.pg_schema,
            "AIRFLOW_REDIS_CONN_URL": self.args.redis_container_name,
            "AIRFLOW_REDIS_CONN_PORT": self.args.redis_container_port,
            "AIRFLOW_REDIS_USER": self.args.redis_user,
            "AIRFLOW_REDIS_PASSWORD": self.args.redis_pass,
            "AIRFLOW_REDIS_SCHEMA": self.args.redis_schema,
            "AIRFLOW__CORE__EXECUTOR": "CeleryExecutor",
            "AIRFLOW__CORE__SQL_ALCHEMY_CONN": f"{self.args.pg_driver}+psycopg2://{self.args.pg_user}:{self.args.pg_password}@{self.args.pg_container_name}:{self.args.pg_container_port}/{self.args.pg_schema}{self.args.pg_extras}",
            "AIRFLOW__CELERY__RESULT_BACKEND": f"db+{self.args.pg_driver}://{self.args.pg_user}:{self.args.pg_password}@{self.args.pg_container_name}:{self.args.pg_container_port}/{self.args.pg_schema}{self.args.pg_extras}",
            "AIRFLOW__CELERY__BROKER_URL": f"{self.args.redis_driver}://{self.args.redis_pass}@{self.args.redis_container_name}/{self.args.redis_schema}",
            "AIRFLOW__CORE__FERNET_KEY": "FpErWX7ZxRBGxuAq2JDfle3A7k7Xxi5hY0wh_u0X0Go=",
            "AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION": "True",
            "AIRFLOW__CORE__LOAD_EXAMPLES": "True",
        }
        if self.args.scheduler_env is not None and isinstance(
            self.args.scheduler_env, dict
        ):
            _scheduler_container_env.update(self.args.scheduler_env)

        _scheduler_container = DockerContainer(
            name=self.args.scheduler_container_name,
            image="{}:{}".format(
                self.args.scheduler_image_name, self.args.scheduler_image_tag
            ),
            command=self.args.scheduler_command,
            # auto_remove=True,
            detach=True,
            entrypoint=self.args.scheduler_entrypoint,
            environment=_scheduler_container_env,
            # remove=True,
            network=docker_build_context.network,
            volumes={
                _airflow_dags_host_dir_path_str: {
                    "bind": self.args.airflow__core__dags_folder,
                    "mode": "rw",
                },
                _airflow_conf_host_dir_path: {
                    "bind": self.args.airflow__core__conf_dir,
                    "mode": "rw",
                },
            },
        )

        _scheduler_rg = DockerResourceGroup(
            name=self.args.scheduler_container_name,
            enabled=self.args.scheduler_enabled,
            weight=102,
            containers=[_scheduler_container],
        )
        # logger.debug("scheduler rg:\n{}".format(_scheduler_rg.json(indent=2)))
        return _scheduler_rg

    def get_webserver_docker_rg(
        self,
        docker_build_context: DockerBuildContext,
    ) -> Optional[DockerResourceGroup]:
        logger.debug(f"Init Webserver DockerResourceGroup")

        _airflow_dags_host_dir_path_str = (
            str(self.args.workspace_dir_path) + self.args.airflow_dags_host_dir_path
        )
        _airflow_conf_host_dir_path = (
            str(self.args.workspace_dir_path) + self.args.airflow_conf_host_dir_path
        )
        _webserver_container_env = {
            "INIT_AIRFLOW_DB": self.args.ws_init_airflow_db,
            "WAIT_FOR_DB": self.args.ws_wait_for_db,
            "WAIT_FOR_REDIS": self.args.ws_wait_for_redis,
            "AIRFLOW_DB_CONN_URL": self.args.pg_container_name,
            "AIRFLOW_DB_CONN_PORT": self.args.pg_container_port,
            "AIRFLOW_DB_USER": self.args.pg_user,
            "AIRFLOW_DB_PASSWORD": self.args.pg_password,
            "AIRFLOW_SCHEMA": self.args.pg_schema,
            "AIRFLOW_REDIS_CONN_URL": self.args.redis_container_name,
            "AIRFLOW_REDIS_CONN_PORT": self.args.redis_container_port,
            "AIRFLOW_REDIS_USER": self.args.redis_user,
            "AIRFLOW_REDIS_PASSWORD": self.args.redis_pass,
            "AIRFLOW_REDIS_SCHEMA": self.args.redis_schema,
            "AIRFLOW__CORE__EXECUTOR": "CeleryExecutor",
            "AIRFLOW__CORE__SQL_ALCHEMY_CONN": f"{self.args.pg_driver}+psycopg2://{self.args.pg_user}:{self.args.pg_password}@{self.args.pg_container_name}:{self.args.pg_container_port}/{self.args.pg_schema}{self.args.pg_extras}",
            "AIRFLOW__CELERY__RESULT_BACKEND": f"db+{self.args.pg_driver}://{self.args.pg_user}:{self.args.pg_password}@{self.args.pg_container_name}:{self.args.pg_container_port}/{self.args.pg_schema}{self.args.pg_extras}",
            "AIRFLOW__CELERY__BROKER_URL": f"{self.args.redis_driver}://{self.args.redis_pass}@{self.args.redis_container_name}/{self.args.redis_schema}",
            "AIRFLOW__CORE__FERNET_KEY": "FpErWX7ZxRBGxuAq2JDfle3A7k7Xxi5hY0wh_u0X0Go=",
            "AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION": "True",
            "AIRFLOW__CORE__LOAD_EXAMPLES": "True",
        }
        if self.args.ws_env is not None and isinstance(self.args.ws_env, dict):
            _webserver_container_env.update(self.args.ws_env)

        _webserver_container = DockerContainer(
            name=self.args.ws_container_name,
            image="{}:{}".format(self.args.ws_image_name, self.args.ws_image_tag),
            command=self.args.ws_command,
            # auto_remove=True,
            detach=True,
            entrypoint=self.args.ws_entrypoint,
            environment=_webserver_container_env,
            # remove=True,
            network=docker_build_context.network,
            ports={
                self.args.ws_container_port: self.args.ws_container_host_port,
            },
            volumes={
                _airflow_dags_host_dir_path_str: {
                    "bind": self.args.airflow__core__dags_folder,
                    "mode": "rw",
                },
                _airflow_conf_host_dir_path: {
                    "bind": self.args.airflow__core__conf_dir,
                    "mode": "rw",
                },
            },
        )

        _webserver_rg = DockerResourceGroup(
            name=self.args.ws_container_name,
            enabled=self.args.ws_enabled,
            weight=103,
            containers=[_webserver_container],
        )
        # logger.debug("webserver rg:\n{}".format(_webserver_rg.json(indent=2)))
        return _webserver_rg

    def get_airflow_docker_rgs(
        self, docker_build_context: DockerBuildContext
    ) -> Optional[List[DockerResourceGroup]]:
        logger.debug(f"Init Airflow DockerResourceGroups")

        airflow_docker_rgs: List[DockerResourceGroup] = []

        # Airflow Database DockerResourceGroup
        if self.args.db_enabled:
            if self.args.db_type == "postgres":
                _pg_docker_rg = self.get_postgres_docker_rg(docker_build_context)
                if _pg_docker_rg is not None:
                    airflow_docker_rgs.append(_pg_docker_rg)

        # Airflow Redis DockerResourceGroup
        if self.args.redis_enabled:
            _redis_docker_rg = self.get_redis_docker_rg(docker_build_context)
            if _redis_docker_rg is not None:
                airflow_docker_rgs.append(_redis_docker_rg)

        # Airflow Scheduler DockerResourceGroup
        if self.args.scheduler_enabled:
            _scheduler_docker_rg = self.get_scheduler_docker_rg(docker_build_context)
            if _scheduler_docker_rg is not None:
                airflow_docker_rgs.append(_scheduler_docker_rg)

        # Airflow Webserver DockerResourceGroup
        if self.args.ws_enabled:
            _webserver_docker_rg = self.get_webserver_docker_rg(docker_build_context)
            if _webserver_docker_rg is not None:
                airflow_docker_rgs.append(_webserver_docker_rg)

        return airflow_docker_rgs

    def init_docker_resource_groups(
        self, docker_build_context: DockerBuildContext
    ) -> None:
        self.docker_resource_groups = OrderedDict()
        # _airflow_rgs: Optional[List[DockerResourceGroup]] = self.get_airflow_docker_rgs(
        #     docker_build_context
        # )
        # if _airflow_rgs is not None:
        #     if self.docker_resource_groups is None:
        #         self.docker_resource_groups = OrderedDict()
        #     for _rg in _airflow_rgs:
        #         self.docker_resource_groups[_rg.name] = _rg
