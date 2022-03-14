import requests



def download(url: str) -> requests.Response:

	response = requests.get(url)
	assert response.ok

	return response