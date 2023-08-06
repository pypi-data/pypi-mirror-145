from pathlib import Path
from typing import Optional, List, Dict, Callable

from pydantic import BaseModel


class RunContext(BaseModel):
    # Run specific variables
    run_date: str
    dry_run: bool = False
    run_status: bool = False
    run_env: Optional[str] = None
    run_env_vars: Optional[Dict[str, str]] = None
    run_params: Optional[Dict[str, str]] = None


class PathContext(BaseModel):
    # Env specific path variables - their values are different on
    # local, docker or cloud environments.
    # These are updated by `phi wf run` for local runs
    # And are provided as Environment variables on containers

    scripts_dir: Optional[Path] = None
    storage_dir: Optional[Path] = None
    meta_dir: Optional[Path] = None
    products_dir: Optional[Path] = None
    notebooks_dir: Optional[Path] = None
    workspace_config_dir: Optional[Path] = None
    workflow_file: Optional[Path] = None
