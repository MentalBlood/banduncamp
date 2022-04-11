import os
import argparse
from typing import Callable
from random import randrange
from functools import partial
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

from .Album import Album
from .Artist import Artist
from .Downloader import Downloader
from .processInParallel import processInParallel



parser = argparse.ArgumentParser(description='Download audio from Bandcamp')
parser.add_argument(
	'url',
	type=str,
	nargs='+',
	help='input page: album URL or discography URL'
)
parser.add_argument(
	'-o',
	'--output',
	default=os.getcwd(),
	dest='output',
	help='output folder path'
)
parser.add_argument(
	'-t',
	'--threads',
	default=2*cpu_count(),
	dest='threads',
	help='number of download threads'
)
parser.add_argument(
	'--downloaded-albums',
	action=argparse.BooleanOptionalAction
)
parser.set_defaults(
	downloaded_albums=True
)
args = parser.parse_args()



def processUrl(url: str, downloader: Downloader, albums_filter: Callable[[str, str], bool]) -> Album | Artist:

	if 'album' in url.split('/'):
		composer = Album.fromUrl
	else:
		composer = partial(Artist.fromUrl, albums_filter=albums_filter)

	return composer(
		url=url,
		downloader=downloader
	)



pool = ThreadPool(int(args.threads))
downloader = Downloader(lambda _: randrange(2, 14) / 10)

objects = processInParallel(
	array=args.url,
	function=lambda u: processUrl(
		url=u,
		downloader=downloader,
		albums_filter=lambda artist, album: not os.path.exists(os.path.join(args.output, artist, album))
	),
	description='Downloading and parsing pages',
	pool=pool
)

tasks = sum([
	o.getDownload(downloader, args.output)
	for o in objects
], start=[])

processInParallel(
	array=tasks,
	function=lambda t: t(),
	description='Downloading covers and tracks',
	pool=pool
)