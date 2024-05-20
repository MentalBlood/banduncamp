import pathlib
import dataclasses

from .Track import Track
from .Album import Album
from .Artist import Artist
from .Pathable import Pathable


@dataclasses.dataclass(frozen=True, kw_only=False)
class Path:

    value: pathlib.Path

    def __truediv__(self, o: Artist | Album | Track | Pathable) -> "Path":
        match o:
            case Pathable():
                return Path(self.value / o)
            case Artist():
                return self / Pathable(o.composer)
            case Album():
                return self / Pathable(o.guessed.name)
            case Track():
                return self / Pathable(f"{o.guessed.title}.mp3")
