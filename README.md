# 🪓 Banduncamp


Fast tool for downloading audio from bandcamp


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


### Album:

```bash
python -m banduncamp <artist_page>/album/<album_name>
```


### Discography:

```bash
python -m banduncamp <artist_page>/music
```

Note that `artist_page` should look like `https://artist.bandcamp.com/`


### Tasks

```bash
python -m banduncamp <path_to_json>
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