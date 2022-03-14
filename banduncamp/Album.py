import os
import re
import json
import html
from typing import Callable
from dataclasses import dataclass

from .Track import Track
from .download import download



@dataclass
class Album:

	title: str
	artist: str
	cover_url: str
	date: str
	tracks: list[Track]

	def download(self, output_folder: str) -> list[Callable[[str], None]]:

		tracks_folder = os.path.join(output_folder, self.title.replace('/', '_'))
		os.makedirs(tracks_folder, exist_ok=True)

		return sum([
			t.download(tracks_folder)
			for t in self.tracks
		], start=[])

	@classmethod
	def fromUrl(_, url):

		page = download(url).text

		data = json.loads(
			html.unescape(
				re.search('data-tralbum=\"([^\"]*)\"', page).group(1)
			)
		)
		cover_url = re.search('<a class="popupImage" href="([^\"]*)', page).group(1)

		return Album(
			artist=data['artist'],
			title=data['current']['title'],
			cover_url=cover_url,
			date=data['current']['release_date'],
			tracks=[
				Track(
					title=track['title'],
					album=data['current']['title'],
					artist=data['artist'],
					url=(track['file'] or {}).get('mp3-128', None),
					number=track['track_num'],
					duration=track['duration'],
					released=not track['unreleased_track']
				)
				for track in data['trackinfo']
			]
		)
