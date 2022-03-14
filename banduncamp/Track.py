import os
import mutagen
from typing import Callable
from functools import partial
from dataclasses import dataclass
from mutagen.easyid3 import EasyID3

from .download import download



@dataclass
class Track:

	title: str
	album: str
	artist: str
	url: str
	number: int
	duration: int
	released: bool

	def _download(self, output_folder: str) -> None:

		file_path = os.path.join(output_folder, f'{self.title}.mp3')
		data = download(self.url).content
		with open(file_path, 'wb') as f:
			f.write(data)

		try:
			tags = EasyID3(file_path)
		except mutagen.id3.ID3NoHeaderError:
			f = mutagen.File(file_path, easy=True)
			f.add_tags()
			tags = f

		tags.update({
			'title': self.title,
			'album': self.album,
			'artist': self.artist,
			'albumartist': self.artist,
			'tracknumber': str(self.number)
		})
		tags.save(file_path, v1=2)
	
	def download(self, output_folder: str) -> list[Callable[[str], None]]:
		return [partial(self._download, output_folder=output_folder)]