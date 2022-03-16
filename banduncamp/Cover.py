import os
from typing import Callable
from functools import partial
from dataclasses import dataclass

from .Downloader import Downloader
from .Downloadable import Downloadable



@dataclass
class Cover(Downloadable):

	url: str
	downloader: Downloader
	file_name: str='cover.jpg'

	def download(self, output_folder: str) -> None:

		path = os.path.join(output_folder, 'cover.jpg')
		if os.path.exists(path):
			return

		self.downloader(self.url, path)

	@classmethod
	def fromUrl(_, url, *args, **kwargs):
		return Cover(
			*args,
			url=url.replace('https', 'http'),
			**kwargs
		)