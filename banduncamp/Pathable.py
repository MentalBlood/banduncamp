import re
import pathlib
import functools
import dataclasses


@dataclasses.dataclass(frozen=True, kw_only=False)
class Pathable:

    source: str

    regex = re.compile(r'[\/\\:\*\?"\<\>|]')

    @functools.cached_property
    def value(self):
        return re.sub(Pathable.regex, "", self.source).strip(". ")[:255].strip(". ")

    def __rtruediv__(self, path: pathlib.Path):
        return path / self.value
