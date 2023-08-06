from typing import Optional

from phidata.asset import DataAsset, DataAssetArgs


class AthenaTableArgs(DataAssetArgs):
    name: str
    database: Optional[str] = None
    catalog: Optional[str] = None
    work_group: Optional[str] = None


class AthenaTable(DataAsset):
    def __init__(
        self,
        name: str,
        database: Optional[str] = None,
        catalog: Optional[str] = None,
        work_group: Optional[str] = None,
        version: Optional[str] = None,
        enabled: bool = True,
    ) -> None:

        super().__init__()
        try:
            self.args: AthenaTableArgs = AthenaTableArgs(
                name=name,
                database=database,
                catalog=catalog,
                work_group=work_group,
                version=version,
                enabled=enabled,
            )
        except Exception as e:
            raise

    @property
    def name(self) -> str:
        return self.args.name

    @property
    def database(self) -> Optional[str]:
        return self.args.database

    @property
    def catalog(self) -> Optional[str]:
        return self.args.catalog

    @property
    def work_group(self) -> Optional[str]:
        return self.args.work_group
