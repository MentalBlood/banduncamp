import os
import re
import json
import html
import argparse
import requests
from tqdm.auto import tqdm
from typing import Callable
from dataclasses import dataclass
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool



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



def getPage(url: str) -> str:

	response = requests.get(url)
	assert response.ok

	return response.text


def downloadFile(url: str, path: str) -> None:

	response = requests.get(url)
	assert response.ok

	with open(path, 'wb') as f:
		f.write(response.content)


@dataclass
class Track:
	number: int
	title: str
	url: str
	duration: int
	released: bool


@dataclass
class Album:
	artist: str
	title: str
	cover_url: str
	date: str
	tracks: list[Track]


def getAlbum(page: str) -> Album:

	data = json.loads(
		html.unescape(
			re.search('data-tralbum=\"([^\"]*)\"', page).group(1)
		)
	)
	cover_url = re.search('<a class="popupImage" href="([^\"]*)', page).group(1)

	return Album(
		artist=data['artist'],
		title=data['current']['title'],
		cover_url=cover_url,
		date=data['current']['release_date'],
		tracks=[
			Track(
				number=track['track_num'],
				title=track['title'],
				url=(track['file'] or {}).get('mp3-128', None),
				duration=track['duration'],
				released=not track['unreleased_track']
			)
			for track in data['trackinfo']
		]
	)


def processInParallel(array: list, function: Callable[[any], any], description: str, threads: int):

	result = []

	for r in tqdm(
			ThreadPool(threads).imap_unordered(
				function,
				array
			),
			desc=description,
			total=len(array)
		):
		result.append(r)

	return result


def composeTrackFileName(track: Track) -> str:
	return f'{track.title}.mp3'


def downloadAlbum(album: Album, output_folder: str, threads: int) -> None:

	tracks_folder = os.path.join(output_folder, album.title)
	os.makedirs(tracks_folder, exist_ok=True)

	processInParallel(
		array=[t for t in album.tracks if t.released],
		function=lambda t: downloadFile(
			url=t.url,
			path=os.path.join(
				tracks_folder,
				composeTrackFileName(t)
			)
		),
		description=f"Downloading album '{album.title}'",
		threads=threads
	)



pages = processInParallel(
	array=args.url,
	function=getPage,
	description='Downloading albums pages',
	threads=args.threads
)

for p in pages:
	album = getAlbum(p)
	downloadAlbum(album, args.output, args.threads)