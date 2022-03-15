import os
from typing import Callable
from functools import partial
from dataclasses import dataclass

from .download import download



@dataclass
class Cover:

	url: str

	def _download(self, output_folder: str) -> None:

		path = os.path.join(output_folder, 'cover.jpg')
		if os.path.exists(path):
			return

		data = download(self.url).content
		with open(path, 'wb') as f:
			f.write(data)

	def download(self, output_folder: str) -> list[Callable[[str], None]]:
		return [partial(self._download, output_folder=output_folder)]