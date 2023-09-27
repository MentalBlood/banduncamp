import requests
import functools
import dataclasses
from bs4 import BeautifulSoup

from .Url import Url



@dataclasses.dataclass(frozen = True, kw_only = False)
class Page:

	url : Url

	@functools.cached_property
	def content(self):
		while not (response := requests.get(self.url.value)).ok:
			print(response)
		return response.content

	@functools.cached_property
	def text(self):
		return self.content.decode()

	@functools.cached_property
	def parsed(self):
		return BeautifulSoup(self.content, 'html.parser', from_encoding = 'utf8')