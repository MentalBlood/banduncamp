import yoop
import pytags
import typing
import functools
import dataclasses

from .Page import Page



@dataclasses.dataclass(frozen = True, kw_only = True)
class Track:

	page    : Page
	guessed : 'Track.Guessed'

	@dataclasses.dataclass(frozen = True, kw_only = True)
	class Guessed:
		title    : str
		album    : str
		artist   : str
		number   : int
		composer : str
		genre    : typing.Iterable[str]

	@functools.cached_property
	def genre(self):
		if len(all := (*self.guessed.genre,)):
			return all[0]
		else:
			return None

	@functools.cached_property
	def data(self):
		return pytags.Tags(
			yoop.Audio(
				pytags.Media(
					self.page.content
				)
			).converted(
				bitrate    = yoop.Audio.Bitrate(128),
				samplerate = yoop.Audio.Samplerate(44100),
				format     = yoop.Audio.Format.MP3,
				channels   = yoop.Audio.Channels.stereo
			).source
		)(
			genre       = '' if self.genre is None else self.genre,
			title       = self.guessed.title,
			album       = self.guessed.album,
			artist      = self.guessed.artist,
			composer    = self.guessed.composer,
			albumartist = self.guessed.artist,
			tracknumber = str(self.guessed.number)
		).source