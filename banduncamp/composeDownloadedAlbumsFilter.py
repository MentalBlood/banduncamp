import os



def composeDownloadedAlbumsFilter(output_folder: str, skip_downloaded_albums: bool):

	if not skip_downloaded_albums:
		return lambda artist, album: False

	def isAlbumDownloaded(artist, album):
		album_path = os.path.join(output_folder, artist, album)
		return not (
			os.path.exists(album_path)
			and any(p.endswith('.mp3') for p in os.listdir(
				album_path
			))
		)

	return isAlbumDownloaded