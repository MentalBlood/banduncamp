from __future__ import annotations

import os
from loguru import _logger
from typing import Callable
from functools import partial

from .Downloader import Downloader



class Downloadable:

	def download(self, downloader: Downloader, output_folder: str, logger: _logger.Logger) -> None:
		pass

	@property
	def children(self) -> list[Downloadable]:
		return []

	def getFolder(self, output_folder: str) -> str:
		return os.path.join(output_folder, self.title)

	def getDownload(self, downloader: Downloader, output_folder: str, logger: _logger.Logger) -> list[Callable[[], None]]:

		result = []

		if self.children:

			children_folder = self.getFolder(output_folder)

			for c in self.children:
				result.extend(c.getDownload(downloader, children_folder, logger))

		result.append(partial(self.download, downloader, output_folder, logger))

		return result