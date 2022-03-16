import os
import re
import json
import html
from typing import Callable
from dataclasses import dataclass

from .Cover import Cover
from .Track import Track
from .Downloader import Downloader
from .correctFileName import correctFileName



@dataclass
class Album:

	title: str
	artist: str
	cover: Cover
	date: str
	tracks: list[Track]

	def download(self, output_folder: str) -> list[Callable[[str], None]]:

		tracks_folder = os.path.join(output_folder, correctFileName(self.title))
		os.makedirs(tracks_folder, exist_ok=True)

		result = []
		result.extend(self.cover.download(tracks_folder))
		for t in self.tracks:
			result.extend(t.download(tracks_folder))

		return result

	@classmethod
	def fromUrl(_, url, downloader: Downloader):

		page = downloader(url).text

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

		return Album(
			artist=data['artist'],
			title=data['current']['title'],
			cover=Cover.fromUrl(
				url=cover_url,
				downloader=downloader
			),
			date=data['current']['release_date'],
			tracks=[
				Track(
					title=track['title'],
					album=data['current']['title'],
					artist=data['artist'],
					url=track['file']['mp3-128'],
					number=track['track_num'],
					duration=track['duration'],
					released=not track['unreleased_track'],
					downloader=downloader
				)
				for track in data['trackinfo']
			]
		)
