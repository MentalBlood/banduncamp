import os
from typing import Callable
from bs4 import BeautifulSoup
from dataclasses import dataclass

from .Album import Album
from .download import download



@dataclass
class Artist:

	title: str
	albums: list[Album]

	def download(self, output_folder: str) -> list[Callable[[str], None]]:

		albums_folder = os.path.join(output_folder, self.title.replace('/', '_'))
		os.makedirs(albums_folder, exist_ok=True)

		return sum([
			a.download(albums_folder)
			for a in self.albums
		], start=[])

	@classmethod
	def fromUrl(_, url):

		page = download(url).text

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
			albums=[
				Album.fromUrl(u)
				for u in albums_urls
			]
		)