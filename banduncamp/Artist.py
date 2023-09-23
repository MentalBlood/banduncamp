import bs4
import functools
import dataclasses

from .Url   import Url
from .Page  import Page
from .Album import Album



@dataclasses.dataclass(frozen=True)
class Artist:

	page : Page

	@functools.cached_property
	def base(self):
		return Url(
			self.page.parsed.find_all(
				'meta',
				{'property': 'og:url'}
			)[0]['content']
		)

	@functools.cached_property
	def composer(self):
		return str(self.page.parsed.find_all('meta', {'property': 'og:title'})[0]['content'])

	@property
	def albums(self):
		return (
			Album(
				page = Page(
					Url(a)
					if (a := element.find_all('a')[0]['href']).startswith('https')
					else self.base / a
				),
				guessed = Album.Guessed(
					name     = element.find_all('p')[0].text.split('\n')[1].strip(),
					composer = self.composer
				)
			)
			for element in self.page.parsed.find_all(id = 'music-grid')[0].children
			if isinstance(element, bs4.Tag)
		)