import os
from typing import Callable
from functools import partial
from dataclasses import dataclass

from .Downloader import Downloader



@dataclass
class Cover:

	url: str
	downloader: Downloader
	file_name: str='cover.jpg'

	def _download(self, output_folder: str) -> None:

		path = os.path.join(output_folder, 'cover.jpg')
		if os.path.exists(path):
			return

		data = self.downloader(self.url).content
		with open(path, 'wb') as f:
			f.write(data)

	def download(self, output_folder: str) -> list[Callable[[str], None]]:
		return [partial(self._download, output_folder=output_folder)]

	@classmethod
	def fromUrl(_, url, *args, **kwargs):
		return Cover(url.replace('https', 'http'), *args, **kwargs)