import os
import requests
import loguru._logger
from time import sleep
from loguru import logger
from typing import Callable
from dataclasses import dataclass



@dataclass
class Downloader:

	getSleepTime: Callable[[int], None]

	def __call__(self, url: str, output: str=None, logger: loguru._logger.Logger = logger) -> requests.Response | None:

		try_number = 1

		while True:

			try:
				response = requests.get(url)
				if response.ok:
					break
			except (
				requests.exceptions.ConnectTimeout,
				requests.exceptions.ConnectionError,
				requests.exceptions.ReadTimeout
			):
				pass

			sleep(self.getSleepTime(try_number))
			try_number += 1

		if output:

			data = response.content
			data_dir = os.dirname(output)
			os.makedirs(data_dir, exist_ok=True)

			try:
				with open(output, 'wb') as f:
					f.write(data)
			except FileNotFoundError as e:
				logger.exception(e)

			return None

		else:
			return response