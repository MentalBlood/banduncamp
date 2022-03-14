import os
import io
import re
import json
import html
import mutagen
import argparse
import requests
from tqdm.auto import tqdm
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from typing import Callable
from mutagen.id3 import TextFrame
from dataclasses import dataclass
from mutagen.easyid3 import EasyID3
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



def download(url: str) -> requests.Response:

	response = requests.get(url)
	assert response.ok

	return response


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

	bar = tqdm(desc=description, total=len(array))

	for r in ThreadPool(threads).imap_unordered(
			function,
			array
		):
		result.append(r)
		bar.update(1)

	return result


def composeTrackFileName(track: Track) -> str:
	return f'{track.title}.mp3'


def downloadTrack(track: Track, album: Album, output_folder: str) -> None:

	file_path = os.path.join(output_folder, composeTrackFileName(track))
	data = download(track.url).content
	with open(file_path, 'wb') as f:
		f.write(data)

	try:
		tags = EasyID3(file_path)
	except mutagen.id3.ID3NoHeaderError:
		f = mutagen.File(file_path, easy=True)
		f.add_tags()
		tags = f

	tags['title'] = track.title
	tags['album'] = album.title
	tags['artist'] = album.artist
	tags['albumartist'] = album.artist
	tags['tracknumber'] = str(track.number)
	tags.save(file_path, v1=2)


def downloadAlbum(album: Album, output_folder: str, threads: int) -> None:

	tracks_folder = os.path.join(output_folder, album.title)
	os.makedirs(tracks_folder, exist_ok=True)

	processInParallel(
		array=album.tracks,
		function=lambda t: downloadTrack(t, album, tracks_folder),
		description=f"Downloading album '{album.title}'",
		threads=threads
	)



pages = processInParallel(
	array=args.url,
	function=lambda u: download(u).text,
	description='Downloading albums pages',
	threads=args.threads
)

for p in pages:
	album = getAlbum(p)
	downloadAlbum(album, args.output, args.threads)