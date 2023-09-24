import typing
import itertools
import dataclasses

from .Path   import Path
from .Track  import Track
from .Album  import Album
from .Artist import Artist



@dataclasses.dataclass(frozen = True, kw_only = False)
class Saved:

	path : Path

	def overwritten(self, track: Track):
		data = track.data.data
		self.path.value.parent.mkdir(parents = True, exist_ok = True)
		self.path.value.write_bytes(data)
		return self

	@typing.overload
	def __call__(self, o: Track) -> typing.Self:
		...

	@typing.overload
	def __call__(self, o: Album | Artist) -> typing.Generator['Saved', None, None]:
		...

	def __call__(self, o: Track | Album | Artist):

		path = self.path / o

		match o:
			case Track():
				if path.value.exists():
					return self
				return Saved(path).overwritten(o)
			case Album():
				if path.value.exists():
					return ()
				return (
					Saved(path)(track)
					for track in o.tracks
				)
			case Artist():
				return itertools.chain.from_iterable(
					Saved(self.path / o)(album)
					for album in o.albums
				)