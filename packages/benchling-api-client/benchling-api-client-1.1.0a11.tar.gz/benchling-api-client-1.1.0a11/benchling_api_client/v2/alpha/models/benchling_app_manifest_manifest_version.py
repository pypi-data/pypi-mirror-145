from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BenchlingAppManifestManifestVersion(Enums.KnownString):
    VALUE_0 = "1"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BenchlingAppManifestManifestVersion":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of BenchlingAppManifestManifestVersion must be a string (encountered: {val})"
            )
        newcls = Enum("BenchlingAppManifestManifestVersion", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(BenchlingAppManifestManifestVersion, getattr(newcls, "_UNKNOWN"))
