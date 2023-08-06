from typing import Optional, Any, Dict, List

from docker.models.images import Image
from docker.errors import BuildError, APIError, ImageNotFound, NotFound

from phidata.infra.docker.api_client import DockerApiClient
from phidata.infra.docker.resource.base import DockerResource
from phidata.utils.cli_console import print_info, print_error
from phidata.utils.log import logger


class DockerImage(DockerResource):
    resource_type: str = "Image"

    # Path to the directory containing the Dockerfile
    path: Optional[str] = None
    # A file object to use as the Dockerfile. (Or a file-like object)
    fileobj: Optional[Any] = None
    # A tag to add to the final image
    tag: Optional[str] = None
    # Whether to return the status
    quiet: Optional[bool] = None
    # Don’t use the cache when set to True
    nocache: Optional[bool] = None
    # Remove intermediate containers.
    # The docker build command defaults to --rm=true,
    # The docker api kept the old default of False to preserve backward compatibility
    rm: Optional[bool] = None
    # HTTP timeout
    timeout: Optional[int] = None
    # Optional if using fileobj
    custom_context: Optional[bool] = None
    # The encoding for a stream. Set to gzip for compressing
    encoding: Optional[str] = None
    # Downloads any updates to the FROM image in Dockerfiles
    pull: Optional[bool] = None
    # Always remove intermediate containers, even after unsuccessful builds
    forcerm: Optional[bool] = None
    # path within the build context to the Dockerfile
    dockerfile: Optional[str] = None
    # A dictionary of build arguments
    buildargs: Optional[Dict[str, Any]] = None
    # A dictionary of limits applied to each container created by the build process. Valid keys:
    # memory (int): set memory limit for build
    # memswap (int): Total memory (memory + swap), -1 to disable swap
    # cpushares (int): CPU shares (relative weight)
    # cpusetcpus (str): CPUs in which to allow execution, e.g. "0-3", "0,1"
    container_limits: Optional[Dict[str, Any]] = None
    # Size of /dev/shm in bytes. The size must be greater than 0. If omitted the system uses 64MB
    shmsize: Optional[int] = None
    # A dictionary of labels to set on the image
    labels: Optional[Dict[str, Any]] = None
    # A list of images used for build cache resolution
    cache_from: Optional[List[Any]] = None
    # Name of the build-stage to build in a multi-stage Dockerfile
    target: Optional[str] = None
    # networking mode for the run commands during build
    network_mode: Optional[str] = None
    # Squash the resulting images layers into a single layer.
    squash: Optional[bool] = None
    # Extra hosts to add to /etc/hosts in building containers, as a mapping of hostname to IP address.
    extra_hosts: Optional[Dict[str, Any]] = None
    # Platform in the format os[/arch[/variant]].
    platform: str = "linux/amd64"
    # Isolation technology used during build. Default: None.
    isolation: Optional[str] = None
    # If True, and if the docker client configuration file (~/.docker/config.json by default)
    # contains a proxy configuration, the corresponding environment variables
    # will be set in the container being built.
    use_config_proxy: Optional[bool] = None

    image_build_id: Optional[str] = None
    # print the build log
    print_build_log: bool = False
    # Push an image or a repository to the registry. Similar to the docker push command.
    push_repo: Optional[str] = None
    # An optional tag to push
    push_tag: Optional[str] = None
    print_push_output: bool = False
    # so that images arent deleted when phi ws down is run
    skip_delete: bool = True

    def build_image(self, docker_client: DockerApiClient) -> Optional[Image]:

        print_info(f"Building image: {self.tag}")
        if self.path is not None:
            print_info(f"\t  path: {self.path}")
        if self.dockerfile is not None:
            print_info(f"    dockerfile: {self.dockerfile}")
        try:
            (image, _build_log_stream) = docker_client.api_client.images.build(
                path=self.path,
                fileobj=self.fileobj,
                tag=self.tag,
                quiet=self.quiet,
                nocache=self.nocache,
                rm=self.rm,
                timeout=self.timeout,
                custom_context=self.custom_context,
                encoding=self.encoding,
                pull=self.pull,
                forcerm=self.forcerm,
                dockerfile=self.dockerfile,
                buildargs=self.buildargs,
                container_limits=self.container_limits,
                shmsize=self.shmsize,
                labels=self.labels,
                cache_from=self.cache_from,
                target=self.target,
                network_mode=self.network_mode,
                squash=self.squash,
                extra_hosts=self.extra_hosts,
                platform=self.platform,
                isolation=self.isolation,
                use_config_proxy=self.use_config_proxy,
            )
            if self.print_build_log:
                for _build_log in _build_log_stream:
                    _stream = _build_log.get("stream", None)
                    if _stream is None or _stream == "\\n":
                        continue
                    if "Step" in _stream:
                        print_info(_stream)
                    if _build_log.get("aux", None) is not None:
                        logger.debug("_build_log['aux'] :{}".format(_build_log["aux"]))
                        self.image_build_id = _build_log.get("aux", {}).get("ID")
            if self.push_repo is not None:
                print_info(f"Pushing {self.push_repo}:{self.push_tag or ''}")
                for _push_output in docker_client.api_client.images.push(
                    repository=self.push_repo,
                    tag=self.push_tag,
                    stream=True,
                    decode=True,
                ):
                    if (
                        self.print_push_output
                        and _push_output.get("status", None) == "Pushing"
                    ):
                        print_info(_push_output.get("progress", None))
                    # if _push_output.get("status", None) == "Pushed":
                    #     print_info("Push complete")
                    if _push_output.get("aux", {}).get("Size", 0) > 0:
                        print_info("Push complete")
                else:
                    docker_client.api_client.images.push(
                        repository=self.push_repo,
                        tag=self.push_tag,
                    )
            return image
        except TypeError as type_error:
            print_error(type_error)
            # print_error("TypeError: {}".format(type_error))
        except BuildError as build_error:
            print_error(build_error)
            # print_error("BuildError: {}".format(build_error))
        except APIError as api_err:
            print_error(api_err)
            # print_error("ApiError: {}".format(api_err))
        return None

    def _create(self, docker_client: DockerApiClient) -> bool:
        """Creates the image

        Args:
            docker_client: The DockerApiClient for the current cluster
        """

        logger.debug("Creating: {}".format(self.get_resource_name()))
        image_object: Optional[Image] = None

        try:
            image_object = self.build_image(docker_client)
            if image_object is not None and isinstance(image_object, Image):
                self.verbose_log("Image built: {}".format(image_object))
                self.active_resource = image_object
                self.active_resource_class = Image
                return True
            else:
                self.verbose_log("Image {} could not be built".format(self.tag))
        except Exception as e:
            logger.exception(e)
            logger.error("Error while creating image: {}".format(e))
            raise

        return False

    def _read(self, docker_client: DockerApiClient) -> Any:
        """Returns an Image object if available"""

        logger.debug("Reading: {}".format(self.get_resource_name()))
        try:
            image_object: Optional[List[Image]] = docker_client.api_client.images.get(
                self.tag
            )
            if image_object is not None and isinstance(image_object, Image):
                self.verbose_log("Image found: {}".format(image_object))
                self.active_resource = image_object
                self.active_resource_class = Image
                return image_object
        except (NotFound, ImageNotFound) as not_found_err:
            self.verbose_log(f"Image {self.tag} not found")

        return None

    def _delete(self, docker_client: DockerApiClient) -> bool:
        """Deletes the Image

        Args:
            docker_client: The DockerApiClient for the current cluster
        """

        logger.debug("Deleting: {}".format(self.get_resource_name()))
        image_object: Optional[Image] = self._read(docker_client)
        # Return True if there is no image to delete
        if image_object is None:
            self.verbose_log("No image to delete")
            return True

        # Delete Image
        try:
            self.active_resource = None
            self.verbose_log("Deleting image: {}".format(self.tag))
            docker_client.api_client.images.remove(image=self.tag, force=True)
            return True
        except Exception as e:
            logger.exception("Error while deleting image: {}".format(e))

        return False
