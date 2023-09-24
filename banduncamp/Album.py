import re
import html
import json
import functools
import dataclasses

from .Url   import Url
from .Page  import Page
from .Track import Track



@dataclasses.dataclass(frozen = True, kw_only = False)
class Album:

	page    : Page
	guessed : 'Album.Guessed'

	@dataclasses.dataclass(frozen = True, kw_only = True)
	class Guessed:
		name     : str
		composer : str

	@functools.cached_property
	def cover(self):
		return Page(
			Url(
				next(
					re.finditer(
						'<a class="popupImage" href="([^\"]*)',
						self.page.text
					)
				).group(1)
			)
		)

	@functools.cached_property
	def composer(self):
		return str(self.page.parsed.find_all(id = 'band-name-location')[0].select('span.title')[0].text)

	@functools.cached_property
	def info(self):
		return json.loads(
			html.unescape(
				re.sub(
					r'\\u\d\d\d\d',
					'',
					next(re.finditer(r'data-tralbum=\"([^\"]*)\"', self.page.text)).group(1)
				)
			)
		)

	@functools.cached_property
	def name(self):
		return str(self.info['current']['title'])

	@functools.cached_property
	def artist(self):
		return str(self.info['artist'])

	@functools.cached_property
	def genres(self):
		return (
			t.text
			for t in self.page.parsed.select('.tag')
		)

	@property
	def tracks(self):
		return (
			Track(
				page = Page(
					Url(
						t['file']['mp3-128']
					)
				),
				guessed = Track.Guessed(
					title    = t['title'],
					album    = self.name,
					genre    = self.genres,
					composer = self.composer,
					artist   = self.artist,
					number   = t['track_num']
				)
			)
			for t in self.info['trackinfo']
			if (
				(not t['unreleased_track']) and
				('file' in t) and
				(t['file'] is not None) and
				('mp3-128' in t['file'])
			)
		)