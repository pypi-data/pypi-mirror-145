from typing import Optional, Dict
from docker.models.containers import Container

from phidata.utils.log import logger


def execute_command(
    cmd: str,
    container: Container,
    wait: bool = True,
    print_output: bool = True,
    docker_env: Optional[Dict[str, str]] = None,
) -> bool:
    import os
    import socket
    import time

    logger.debug("Exec `{}` in container: {}".format(cmd, container.name))
    _container_socket: Optional[socket.SocketIO] = None
    exit_code, _container_socket = container.exec_run(
        cmd=cmd,
        stdout=True,
        stdin=True,
        tty=True,
        socket=True,
        environment=docker_env,
    )

    if _container_socket is None:
        logger.debug("container_socket is None")
        return False

    if not (wait or print_output):
        return True

    if _container_socket.readable():
        # code references the following
        # - https://stackoverflow.com/a/66329671
        # logger.debug("_container_socket is readable")
        _container_socket._sock.setblocking(False)  # type: ignore

        _op = None
        while True:
            try:
                _op = os.read(_container_socket.fileno(), 8192)
                # logger.debug("Op: {}".format(_op))
            except BlockingIOError as not_ready_error:
                # logger.exception(not_ready_error)
                logger.info("waiting...")
                time.sleep(1)
                continue

            if _op is None:
                logger.info("Output not available.")
                break
            if (
                _op == b""
                or (isinstance(_op, bytes) and _op.decode(errors="ignore")) == ""
            ):
                logger.info("Task finished")
                break

            # Use print here because console.print has issues decoding output
            if print_output:
                print(_op.decode(errors="ignore"))

    return True
