import os
import argparse
from tqdm.auto import tqdm
from typing import Callable
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

from .Album import Album
from .Artist import Artist
from .download import download



parser = argparse.ArgumentParser(description='Download audio from Bandcamp')
parser.add_argument(
	'url',
	type=str,
	nargs='+',
	help='input page URL'
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



def processInParallel(array: list, function: Callable[[any], any], description: str, pool: ThreadPool):

	result = []

	bar = tqdm(desc=description, total=len(array))

	for r in pool.imap_unordered(function, array):
		result.append(r)
		bar.update(1)

	return result


def processUrl(url: str) -> Album | Artist:

	if 'album' in url.split('/'):
		C = Album
	else:
		C = Artist

	return C.fromUrl(url)



pool = ThreadPool(args.threads)

objects = processInParallel(
	array=args.url,
	function=lambda u: processUrl(u),
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
	description='Downloading tracks',
	pool=pool
)