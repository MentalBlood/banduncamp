import requests
from time import sleep
from random import randrange



def download(url: str) -> requests.Response:

	response = requests.get(url)

	while not response.ok:
		sleep(randrange(4, 20) / 10)
		response = requests.get(url)

	return response