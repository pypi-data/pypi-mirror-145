from pathlib import Path
from typing import Optional, Union, Any

from phidata.asset import DataAsset, DataAssetArgs
from phidata.utils.cli_console import print_error
from phidata.utils.enums import ExtendedEnum
from phidata.utils.log import logger
from phidata.utils.filesystem import delete_from_fs


class FileType(ExtendedEnum):
    CSV = "CSV"
    TSV = "TSV"
    TXT = "TXT"
    JSON = "JSON"


class FileArgs(DataAssetArgs):
    name: Optional[str]
    # parent directory of the file relative to the base_dir
    file_dir: Optional[Union[str, Path]]
    file_type: Optional[FileType]
    # absolute path for the file
    file_path: Optional[Path]


class File(DataAsset):
    def __init__(
        self,
        name: Optional[str] = None,
        # parent directory of the file relative to the base_dir
        file_dir: Optional[Union[str, Path]] = None,
        file_type: Optional[FileType] = None,
        # absolute path for the file
        file_path: Optional[Path] = None,
        version: Optional[str] = None,
        enabled: bool = True,
    ) -> None:

        super().__init__()
        try:
            self.args: FileArgs = FileArgs(
                name=name,
                file_dir=file_dir,
                file_type=file_type,
                file_path=file_path,
                version=version,
                enabled=enabled,
            )
        except Exception as e:
            print_error(f"Args for {self.__class__.__name__} are not valid")
            raise

    @property
    def file_dir(self) -> Optional[Union[str, Path]]:
        return self.args.file_dir

    @file_dir.setter
    def file_dir(self, file_dir: Union[str, Path]) -> None:
        if file_dir is not None:
            self.args.file_dir = file_dir

    @property
    def file_type(self) -> Optional[FileType]:
        if self.args.file_type is not None:
            return self.args.file_type

        # logger.debug("-*--*- Building file_type")
        fp = self.file_path
        if fp is None:
            return None
        suffix = fp.suffix[1:]  # remove the . from ".json" or ".csv"
        # logger.debug("suffix: {}".format(suffix))

        derived_file_type: Optional[FileType] = None
        if suffix.upper() in FileType.values_list():
            derived_file_type = FileType.from_str(suffix.upper())
            self.args.file_type = derived_file_type
        return self.args.file_type

    @file_type.setter
    def file_type(self, file_type: Optional[FileType]) -> None:
        if file_type is not None:
            self.args.file_type = file_type

    @property
    def file_path(self) -> Optional[Path]:
        if self.args.file_path is not None:
            return self.args.file_path

        # logger.debug("-*--*- Building file_path")
        # Start with the base_dir_path
        # base_dir_path is loaded from the current environment variable
        _file_path: Optional[Path] = self.base_dir_path
        # Add the file_dir if available
        if self.file_dir is not None:
            if _file_path is None:
                # _file_path is None meaning no base_dir_path
                _file_path = Path(self.file_dir)
            else:
                _file_path = _file_path.joinpath(self.file_dir)

        # Add the file_name
        if self.name is not None:
            if _file_path is None:
                _file_path = Path(self.name)
            else:
                _file_path = _file_path.joinpath(self.name)

        self.args.file_path = _file_path
        return self.args.file_path

    ######################################################
    ## Write to file
    ######################################################

    def write_pandas_df(self, df: Any = None) -> bool:
        # File not yet initialized
        if self.args is None:
            return False

        # Check path is available
        if self.file_path is None:
            print_error("FilePath invalid")
            return False

        # write to file
        import pandas as pd

        if df is None or not isinstance(df, pd.DataFrame):
            print_error("DataFrame invalid")
            return False

        file_path: Path = self.file_path
        logger.debug("Writing DF to file: {}".format(file_path))
        if file_path.exists():
            logger.debug("Deleting: {}".format(file_path))
            delete_from_fs(file_path)

        if not file_path.exists():
            logger.debug("Creating: {}".format(file_path))
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch(exist_ok=True)

        try:
            with file_path.open("w") as open_file:
                logger.debug("file_type: {}".format(self.file_type))
                if self.file_type == FileType.JSON:
                    df.to_json(open_file, orient="index", indent=4)
                elif self.file_type == FileType.JSON:
                    df.to_csv(open_file)
                else:
                    print_error(f"{self.file_type.value} not yet supported")
                    return False
        except Exception as e:
            raise

        return True
