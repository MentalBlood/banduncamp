from __future__ import annotations

import os
from typing import Callable
from functools import partial
from dataclasses import dataclass

from .correctFileName import correctFileName



@dataclass
class Downloadable:

	def download(self, output_folder: str) -> None:
		pass

	@property
	def children(self) -> list[Downloadable]:
		return []

	def getFolder(self, output_folder: str) -> str:
		return os.path.join(output_folder, correctFileName(self.title))

	def getDownload(self, output_folder, *args, **kwargs) -> list[Callable[[], None]]:

		result = [partial(self.download, output_folder, *args, **kwargs)]

		if self.children:

			children_folder = self.getFolder(output_folder)
			os.makedirs(children_folder)

			for c in self.children:
				result.extend(c.getDownload(children_folder))

		return result