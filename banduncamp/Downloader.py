import requests
from time import sleep
from typing import Callable
from dataclasses import dataclass



@dataclass
class Downloader:

	getSleepTime: Callable[[int], None]
	exceptions: tuple[Exception]=(requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError)

	def __call__(self, url: str, output: str=None) -> requests.Response | None:

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

		if output:

			data = response.content
			with open(output, 'wb') as f:
				f.write(data)

			return None

		else:
			return response