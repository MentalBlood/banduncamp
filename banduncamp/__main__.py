import os
import argparse
from random import randrange
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
args = parser.parse_args()



def processUrl(url: str, downloader: Downloader) -> Album | Artist:

	if 'album' in url.split('/'):
		C = Album
	else:
		C = Artist

	return C.fromUrl(
		url=url,
		downloader=downloader
	)



pool = ThreadPool(int(args.threads))
downloader = Downloader(lambda _: randrange(2, 14) / 10)

objects = processInParallel(
	array=args.url,
	function=lambda u: processUrl(u, downloader),
	description='Downloading and parsing pages',
	pool=pool
)

tasks = sum([
	o.download(args.output)
	for o in objects
], start=[])

processInParallel(
	array=tasks,
	function=lambda t: t(),
	description='Downloading covers and tracks',
	pool=pool
)