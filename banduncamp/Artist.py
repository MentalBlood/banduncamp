from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

from .Album import Album
from .Downloader import Downloader
from .Downloadable import Downloadable
from .processInParallel import processInParallel



@dataclass
class Artist(Downloadable):

	title: str
	albums: list[Album]

	@property
	def children(self):
		return self.albums

	@classmethod
	def fromUrl(_, url, downloader: Downloader, pool=None):

		page = downloader(url).text

		root = BeautifulSoup(page, 'html.parser')

		grid_items = filter(
			lambda c: isinstance(c, Tag),
			root.find(id='music-grid').children
		)

		base_url = root.find('meta', {'property': 'og:url'})['content']
		albums_urls = [
			f"{base_url}{g.find('a')['href']}"
			for g in grid_items
		]

		artist_title = root.find('meta', {'property': 'og:title'})['content']

		return Artist(
			title=artist_title,
			albums=processInParallel(
				array=albums_urls,
				function=lambda u: Album.fromUrl(u, downloader),
				description=f"Downloading '{artist_title}' albums pages",
				pool=pool or ThreadPool(cpu_count())
			)
		)