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

		page = downloader(url).text

		composers = {
			'album': Album.fromPage,
			'artist': partial(Artist.fromPage, downloader=downloader, albums_filter=albums_filter)
		}

		if 'album' in url.split('/'):
			proposed = 'album'
		else:
			proposed = 'artist'

		try:
			result = composers[proposed](page=page)
			return result
		except:
			for another in composers.keys():
				if another != proposed:
					try:
						result = composers[another](page=page)
						return result
					except:
						pass

		raise TypeError(f'No composer found among {[*composers.keys()]} for URL: {url}')