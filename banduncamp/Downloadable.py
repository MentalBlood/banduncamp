from __future__ import annotations

import os
from typing import Callable
from functools import partial
from dataclasses import dataclass

from .Downloader import Downloader
from .correctFileName import correctFileName



@dataclass
class Downloadable:

	def download(self, downloader: Downloader, output_folder: str) -> None:
		pass

	@property
	def children(self) -> list[Downloadable]:
		return []

	def getFolder(self, output_folder: str) -> str:
		return os.path.join(output_folder, correctFileName(self.title))

	def getDownload(self, downloader: Downloader, output_folder: str) -> list[Callable[[], None]]:

		result = [partial(self.download, downloader, output_folder)]

		if self.children:

			children_folder = self.getFolder(output_folder)
			try:
				os.makedirs(children_folder)
			except FileExistsError:
				pass

			for c in self.children:
				result.extend(c.getDownload(downloader, children_folder))

		return result