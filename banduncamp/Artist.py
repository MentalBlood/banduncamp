from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

from .Album import Album
from .Downloader import Downloader
from .Downloadable import Downloadable
from .correctFileName import correctFileName
from .processInParallel import processInParallel



@dataclass
class Artist(Downloadable):

	title: str
	albums: list[Album]

	@property
	def children(self):
		return self.albums

	@classmethod
	def fromPage(_, page: str, downloader: Downloader, pool=None, albums_filter=(lambda artist, album: True)):

		root = BeautifulSoup(page, 'html.parser')

		artist_title = root.find('meta', {'property': 'og:title'})['content']

		grid_items = filter(
			lambda c: isinstance(c, Tag),
			root.find(id='music-grid').children
		)

		base_url = root.find('meta', {'property': 'og:url'})['content']

		albums_urls = {}
		for g in grid_items:

			name = g.find('p').text.split('\n')[1].strip()
			if not albums_filter(
				correctFileName(artist_title),
				correctFileName(name)
			):
				continue

			a = g.find('a')['href']
			if a.startswith('https'):
				url = a
			else:
				url = f"{base_url}{a}"

			albums_urls[name] = url

		return Artist(
			title=artist_title,
			albums=processInParallel(
				array=[*albums_urls.values()],
				function=lambda u: Album.fromPage(downloader(u).text),
				description=f"Downloading '{artist_title}' albums pages",
				pool=pool or ThreadPool(cpu_count())
			)
		)