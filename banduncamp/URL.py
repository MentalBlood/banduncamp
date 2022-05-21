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

		composers = {
			'album': Album.fromUrl,
			'artist': partial(Artist.fromUrl, albums_filter=albums_filter)
		}

		if 'album' in url.split('/'):
			proposed = 'album'
		else:
			proposed = 'artist'

		try:
			result = composers[proposed](
				url=url,
				downloader=downloader
			)
		except:
			for another in composers.keys():
				if another != proposed:
					try:
						result = composers[another](
							url=url,
							downloader=downloader
						)
						return result
					except:
						pass

		raise TypeError(f'No composer found among {[*composers.keys()]} for URL: {url}')