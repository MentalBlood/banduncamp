import requests
from time import sleep
from random import randrange



def download(url: str) -> requests.Response:

	while True:

		try:
			response = requests.get(url)
			if response.ok:
				break
		except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
			pass

		sleep(randrange(2, 14) / 10)

	return response