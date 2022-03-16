import requests
from time import sleep
from typing import Callable
from dataclasses import dataclass



@dataclass
class Downloader:

	getSleepTime: Callable[[int], None]
	exceptions: tuple[Exception]=(requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError)

	def __call__(self, url: str) -> requests.Response:

		try_number = 1

		while True:

			try:
				response = requests.get(url)
				if response.ok:
					break
			except :
				pass

			sleep(self.getSleepTime(self.try_number))
			try_number += 1

		return response