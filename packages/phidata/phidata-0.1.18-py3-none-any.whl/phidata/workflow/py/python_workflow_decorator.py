from functools import wraps, partial

from phidata.workflow.py.python_workflow import PythonWorkflow
from phidata.utils.cli_console import print_error
from phidata.utils.log import logger


def create_workflow(func):
    """Converts a function into a python workflow"""

    wraps(func)

    def wrapper(*args, **kwargs):
        # logger.info(f"args: {args}")
        # logger.info(f"kwargs: {kwargs}")
        try:
            name = kwargs.get("name", func.__name__)
            entrypoint = partial(func, *args, **kwargs)

            non_null_args = {}
            if "task_id" in kwargs:
                non_null_args["task_id"] = kwargs["task_id"]
            if "dag_id" in kwargs:
                non_null_args["dag_id"] = kwargs["dag_id"]
            if "version" in kwargs:
                non_null_args["version"] = kwargs["version"]
            if "enabled" in kwargs:
                non_null_args["enabled"] = kwargs["enabled"]
            if "engine" in kwargs:
                non_null_args["engine"] = kwargs["engine"]

            wf = PythonWorkflow(name=name, entrypoint=entrypoint, **non_null_args)
            return wf
        except Exception as e:
            print_error("Could not create workflow for: {}".format(func))
            print_error(e)

    return wrapper


"""
How to use create_workflow:

@create_workflow
def test_wf(param, **kwargs):
    return True

wf = test_wf(param="yum")

dp = DataProduct(name="dp", workflows=[wf])
"""
