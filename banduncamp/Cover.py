import os
from dataclasses import dataclass

from .Downloadable import Downloadable



@dataclass
class Cover(Downloadable):

	url: str
	file_name: str='cover.jpg'

	def download(self, downloader, output_folder) -> None:

		path = os.path.join(output_folder, 'cover.jpg')
		if os.path.exists(path):
			return

		downloader(self.url, path)

	@classmethod
	def fromUrl(_, url):
		return Cover(url.replace('https', 'http'))