import os
import re
import json
import html
import mutagen
import argparse
import requests
from tqdm.auto import tqdm
from typing import Callable
from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag
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


def processInParallel(array: list, function: Callable[[any], any], description: str, pool: ThreadPool):

	result = []

	bar = tqdm(desc=description, total=len(array))

	for r in pool.imap_unordered(
			function,
			array
		):
		result.append(r)
		bar.update(1)

	return result


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


@dataclass
class Artist:
	title: str
	albums: list[Album]


@dataclass
class DownloadTrackTask:
	track: Track
	album: Album
	output_folder: str


def parseAlbumPage(page: str) -> Album:

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


def parseArtistPage(page: str, pool: ThreadPool) -> Artist:

	root = BeautifulSoup(page, 'html.parser')

	grid_items = filter(
		lambda c: isinstance(c, Tag),
		root.find(id='music-grid').children
	)

	base_url = root.find('meta', {'property': 'og:url'})['content']
	albums_urls = [
		f"{base_url}{g.find('a')['href']}"
		for g in grid_items
	]

	artist_title = root.find('meta', {'property': 'og:title'})['content']

	albums = processInParallel(
		array=albums_urls,
		function=lambda u: parseAlbumPage(download(u).text),
		description=f"Parsing albums pages for artist '{artist_title}'",
		pool=pool
	)

	return Artist(
		title=artist_title,
		albums=albums
	)


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


def composeAlbumDownloadTasks(album: Album, output_folder: str, pool: ThreadPool) -> list[DownloadTrackTask]:

	tracks_folder = os.path.join(output_folder, album.title.replace('/', '_'))
	os.makedirs(tracks_folder, exist_ok=True)
	
	return [
		DownloadTrackTask(
			track=t,
			album=album,
			output_folder=tracks_folder
		)
		for t in album.tracks
	]


def composeArtistDownloadTasks(artist: Artist, output_folder: str, pool: ThreadPool) -> list[DownloadTrackTask]:

	albums_folder = os.path.join(output_folder, artist.title.replace('/', '_'))
	os.makedirs(albums_folder, exist_ok=True)

	return sum([
		composeAlbumDownloadTasks(a, albums_folder, pool)
		for a in artist.albums
	], start=[])


def processUrl(url: str, pool: ThreadPool) -> Album | Artist:

	page = download(url).text

	if 'album' in url.split('/'):
		result = parseAlbumPage(page)
	else:
		result = parseArtistPage(page, pool)

	return result


def composeDownloadTasks(o: Album | Artist, output: str, pool: ThreadPool) -> list[DownloadTrackTask]:
	if isinstance(o, Album):
		return composeAlbumDownloadTasks(o, output, pool)
	elif isinstance(o, Artist):
		return composeArtistDownloadTasks(o, output, pool)



pool = ThreadPool(args.threads)

objects = processInParallel(
	array=args.url,
	function=lambda u: processUrl(u, pool),
	description='Downloading and parsing pages',
	pool=pool
)

tasks = sum([
	composeDownloadTasks(o, args.output, pool)
	for o in objects
], start=[])

processInParallel(
	array=tasks,
	function=lambda t: downloadTrack(**t.__dict__),
	description='Downloading tracks',
	pool=pool
)