import click
import pathlib

from .Url    import Url
from .Path   import Path
from .Page   import Page
from .Saved  import Saved
from .Artist import Artist



@click.group
def cli():
	pass



@cli.command(name = 'artist')
@click.option('--url',  required = True, type = Url,          help = 'address of artist music page')
@click.option('--root', required = True, type = pathlib.Path, help = 'path to save folder with albums to')
def artist(url: Url, root: pathlib.Path):
	for s in Saved(Path(root))(Artist(Page(url))):
		print(str(s.path.value))



cli()