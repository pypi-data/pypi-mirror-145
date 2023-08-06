from collections import namedtuple

RunStatus = namedtuple("RunStatus", ["name", "success"], defaults=[False])
