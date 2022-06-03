import re
import json
import html
from bs4 import BeautifulSoup
from dataclasses import dataclass

from .Cover import Cover
from .Track import Track
from .Downloader import Downloader
from .Downloadable import Downloadable



@dataclass
class Album(Downloadable):

	title: str
	artist: str
	composer: str
	cover: Cover
	date: str
	tracks: list[Track]
	
	@property
	def children(self):
		return [self.cover, *self.tracks]

	@classmethod
	def fromPage(_, page: str):

		data = json.loads(
			html.unescape(
				re.sub(
					r'\\u\d\d\d\d',
					'',
					re.search(r'data-tralbum=\"([^\"]*)\"', page).group(1)
				)
			)
		)
		cover_url = re.search('<a class="popupImage" href="([^\"]*)', page).group(1)

		root = BeautifulSoup(page, 'html.parser')
		band_name_tag = root.find(id='band-name-location')
		composer = band_name_tag.select('span.title')[0].text

		tracks = []
		for t in data['trackinfo']:
			try:
				tracks.append(Track(
					title=t['title'],
					album=data['current']['title'],
					artist=data['artist'],
					composer=composer,
					url=t['file']['mp3-128'],
					number=t['track_num'],
					duration=t['duration'],
					released=not t['unreleased_track']
				))
			except (TypeError, KeyError):
				pass

		return Album(
			artist=data['artist'],
			composer=composer,
			title=data['current']['title'],
			cover=Cover.fromUrl(cover_url),
			date=data['current']['release_date'],
			tracks=tracks
		)
