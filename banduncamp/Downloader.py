import requests
from time import sleep
from typing import Callable
from dataclasses import dataclass



@dataclass
class Downloader:

	getSleepTime: Callable[[int], None]

	def __call__(self, url: str, output: str=None) -> requests.Response | None:

		try_number = 1

		while True:

			try:
				response = requests.get(url)
				if response.ok:
					break
			except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
				pass

			sleep(self.getSleepTime(try_number))
			try_number += 1

		if output:

			data = response.content
			with open(output, 'wb') as f:
				f.write(data)

			return None

		else:
			return response