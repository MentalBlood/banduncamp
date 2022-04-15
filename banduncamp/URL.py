from typing import Callable
from functools import partial

from .Album import Album
from .Artist import Artist
from .Downloader import Downloader



class URL(str):

	def download(
		url: str,
		downloader: Downloader,
		albums_filter: Callable[[str, str], bool]
	) -> Album | Artist:

		if 'album' in url.split('/'):
			composer = Album.fromUrl
		else:
			composer = partial(Artist.fromUrl, albums_filter=albums_filter)

		return composer(
			url=url,
			downloader=downloader
		)