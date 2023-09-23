import click
import pathlib

from .Url     import Url
from .Page    import Page
from .Artist   import Artist
from .Pathable import Pathable



@click.group
def cli():
	pass



@cli.command(name = 'artist')
@click.option('--url',  required = True, type = Url,          help = 'address of artist music page')
@click.option('--root', required = True, type = pathlib.Path, help = 'path to save albums to')
def artist(url : Url, root: pathlib.Path):

	for album in (artist := Artist(Page(url))).albums:

		if pathlib.Path(
			root /
			Pathable(artist.composer) /
			Pathable(album.guessed.name)
		).exists():
			continue

		for track in album.tracks:

			if (
				path := pathlib.Path(
					root /
					Pathable(artist.composer) /
					Pathable(album.name) /
					f'{Pathable(track.guessed.title).value}.mp3'
				)
			).exists():
				continue

			path.parent.mkdir(parents = True, exist_ok = True)
			path.write_bytes(track.data.data)
			print(str(path))



cli()