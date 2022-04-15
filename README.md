# 🪓 Banduncamp

Fast. Stubborn. Tool for downloading audio from bandcamp

## Installation

```bash
pip install git+https://github.com/MentalBlood/banduncamp
```

## Usage

To get help:

```bash
python -m banduncamp -h
```

Tool will not download audio file if it already exists

Tool will not download album if corresponding dir already exists. Use `--no-skip-downloaded-albums` to override this

### Album:

```bash
python -m banduncamp <album_page>
```

Note that `album_page` should look like `https://artist_name.bandcamp.com/album/album_name`

### Discography:

```bash
python -m banduncamp <artist_page>
```

Note that `artist_page` should look like `https://artist_name.bandcamp.com/music`

### Tasks

```bash
python -m banduncamp -f <path_to_json>
```

JSON should be like:

```json
{
    "D:/music/Ambient": [
        "https://lalala.bandcamp.com/music",
        "https://lololo.bandcamp.com/music"
    ],
    "D:/music/Dungeon Synth": [
        "https://lululu.bandcamp.com/music",
        "https://lilili.bandcamp.com/music"
    ]
}
```

## Bugs

No known, if found please report [here](https://github.com/MentalBlood/banduncamp/issues)