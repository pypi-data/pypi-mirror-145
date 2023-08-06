from pathlib import Path
from typing import Optional, Any

from pydantic import BaseModel

from phidata.constants import STORAGE_DIR_ENV_VAR
from phidata.utils.log import logger


class DataAssetArgs(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None
    enabled: bool = True

    # The base_dir_path is the root dir for the data_asset.
    # It depends on the environment (local vs container) and is
    # used by the data_asset to build the absolute path in different environments
    base_dir_path: Optional[Path] = None

    debug_on: bool = True

    class Config:
        arbitrary_types_allowed = True


class DataAsset:
    """Base Class for all DataAssets"""

    def __init__(self) -> None:
        self.args: Optional[DataAssetArgs] = None

    @property
    def name(self) -> str:
        return (
            self.args.name if self.args and self.args.name else self.__class__.__name__
        )

    @property
    def version(self) -> Optional[str]:
        return self.args.version if self.args else None

    @property
    def enabled(self) -> bool:
        return self.args.enabled if self.args else False

    @property
    def base_dir_path(self) -> Optional[Path]:
        """
        Returns the base dir for the data_asset.
        This base dir depends on the environment (local vs container) and is
        used by the data_asset to build the absolute path.
        """
        # data_asset not yet initialized
        if self.args is None:
            return None

        if self.args.base_dir_path:
            # use cached value if available
            return self.args.base_dir_path

        # logger.debug(f"Loading {STORAGE_DIR_ENV_VAR} from env")
        import os

        storage_dir_env = os.getenv(STORAGE_DIR_ENV_VAR)
        # logger.debug(f"{STORAGE_DIR_ENV_VAR}: {storage_dir_env}")
        if storage_dir_env is not None:
            self.args.base_dir_path = Path(storage_dir_env)
        return self.args.base_dir_path

    @base_dir_path.setter
    def base_dir_path(self, data_dir_path: Optional[Path]) -> None:
        if self.args is not None and data_dir_path is not None:
            self.args.base_dir_path = data_dir_path

    ######################################################
    ## Build and validate data asset
    ######################################################

    def build(self) -> bool:
        logger.debug(f"@build not defined for {self.__class__.__name__}")
        return False

    ######################################################
    ## Write to DataAsset
    ######################################################

    def write_pandas_df(self, df: Any = None) -> bool:
        logger.debug(f"@write_pandas_df not defined for {self.__class__.__name__}")
        return False

    ######################################################
    ## Print
    ######################################################

    def __str__(self) -> str:
        if self.args is not None:
            return self.args.json(indent=2, exclude_none=True, exclude={"enabled"})
        else:
            return self.__class__.__name__
