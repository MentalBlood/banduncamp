import os
import json
import argparse
from typing import Callable
from random import randrange
from operator import methodcaller
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

from .URL import URL
from .Downloader import Downloader
from .processInParallel import processInParallel



parser = argparse.ArgumentParser(description='Download audio from Bandcamp')
parser.add_argument(
	'url',
	type=URL,
	nargs='*',
	help='input page: album URL or discography URL'
)
parser.add_argument(
	'-f',
	'--file',
	type=str,
	nargs='*',
	help='JSON file with output-to-URLs mapping'
)
parser.add_argument(
	'-o',
	'--output',
	default=os.getcwd(),
	help='output folder path'
)
parser.add_argument(
	'-t',
	'--threads',
	default=2*cpu_count(),
	help='number of download threads'
)
parser.add_argument(
	'--skip-downloaded-albums',
	action=argparse.BooleanOptionalAction
)
parser.set_defaults(
	skip_downloaded_albums=True
)
args = parser.parse_args()



def downloadByUrls(
	urls: list[str],
	output: str,
	downloader: Downloader,
	albums_filter: Callable[[str, str], bool],
	pool: ThreadPool
):

	objects = processInParallel(
		array=urls,
		function=methodcaller(
			'download',
			downloader=downloader,
			albums_filter=albums_filter
		),
		description='Downloading and parsing pages',
		pool=pool
	)

	tasks = []
	for o in objects:
		o_tasks = o.getDownload(downloader, output)
		tasks.extend(o_tasks)

	processInParallel(
		array=tasks,
		function=lambda t: t(),
		description='Downloading covers and tracks',
		pool=pool
	)


output_to_urls = {}

if args.url:
	output_to_urls[args.output] = args.url

if args.file:
	for path in args.file or []:
		with open(path) as f:
			for o, urls in json.load(f).items():
				if o not in output_to_urls:
					output_to_urls[o] = []
				for u in urls:
					output_to_urls[o].append(URL(u))

pool = ThreadPool(int(args.threads))
downloader = Downloader(getSleepTime=lambda _: randrange(2, 14) / 10)


for o, u in output_to_urls.items():
	downloadByUrls(
		urls=u,
		output=o,
		downloader=downloader,
		albums_filter=(
			lambda artist, album:
				not args.skip_downloaded_albums
				or not os.path.exists(
					os.path.join(o, artist, album)
				)
		),
		pool=pool
	)