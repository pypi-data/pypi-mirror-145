# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pymtheg']
install_requires = \
['rich>=11.2.0,<12.0.0', 'spotdl>=3.9.3,<4.0.0']

entry_points = \
{'console_scripts': ['pymtheg = pymtheg:main']}

setup_kwargs = {
    'name': 'pymtheg',
    'version': '2.3.0',
    'description': 'A Python script to share songs from Spotify/YouTube as a 15 second clip.',
    'long_description': '# pymtheg\n\nA Python script to share songs from Spotify/YouTube as a 15 second clip.\n[Designed for use with Termux.](https://github.com/markjoshwel/pymtheg/blob/main/TERMUX.md)\n\nSee the [repository](https://github.com/markjoshwel/pymtheg) for more installation and\ncontribution instructions/information.\n\n[![asciicast](https://asciinema.org/a/483803.svg)](https://asciinema.org/a/483803)\n\n## Installation\n\npymtheg requires [Python 3.6.2](https://python.org/) or later, and\n[ffmpeg](https://ffmpeg.org/).\n\n## Usage\n\n```text\nusage: pymtheg [-h] [-d DIR] [-o OUT] [-tf TIMESTAMP_FORMAT] [-e EXT] [-sda SDARGS] [-ffa FFARGS]\n               [-cs CLIP_START] [-ce CLIP_END] [-i IMAGE] [-ud] [-y]\n               queries [queries ...]\n\na python script to share songs from Spotify/YouTube as a 15 second clip\n\npositional arguments:\n  queries               song queries (see querying)\n\noptions:\n  -h, --help            show this help message and exit\n  -d DIR, --dir DIR     directory to output to, formattable (see formatting)\n  -o OUT, --out OUT     output file name format, formattable (see formatting)\n  -tf TIMESTAMP_FORMAT, --timestamp-format TIMESTAMP_FORMAT\n                        timestamp format, formattable (see formatting)\n  -e EXT, --ext EXT     file extension, defaults to "mp4"\n  -sda SDARGS, --sdargs SDARGS\n                        args to pass to spotdl\n  -ffa FFARGS, --ffargs FFARGS\n                        args to pass to ffmpeg for clip creation\n  -cs CLIP_START, --clip-start CLIP_START\n                        specify clip start (default 0)\n  -ce CLIP_END, --clip-end CLIP_END\n                        specify clip end (default +15)\n  -i IMAGE, --image IMAGE\n                        specify custom image\n  -ud, --use-defaults   use 0 as clip start and --clip-length as clip end\n  -y, --yes             say yes to every y/n prompt\n\nquerying:\n  queries are passed onto spotdl, and thus must be any one of the following:\n    1. text\n      "<query>"\n      e.g. "thundercat - them changes"\n    2. spotify track/album url\n      "<url>"\n      e.g. "https://open.spotify.com/track/..."\n    3. youtube source + spotify metadata\n      "<youtube url>|<spotify url>"\n      e.g. "https://www.youtube.com/watch?v=...|https://open.spotify.com/track/..."\n\nargument defaults:\n  -f, --ffargs:\n    "-hide_banner -loglevel error -c:a aac -c:v libx264 -pix_fmt yuv420p -tune stillimage -vf scale=\'iw+mod(iw,2):ih+mod(ih,2):flags=neighbor\'"\n  -o, --out:\n    "{artists} - {title}"\n  -t, --timestamp-format:\n     ({cs}{cer})\n\nformatting:\n  available placeholders:\n    from spotdl:\n      {artist}, {artists}, {title}, {album}, {playlist}\n    from pymtheg:\n      {cs}\n        clip end as per [(h*)mm]ss, e.g. 10648 (1h, 06m, 48s)\n      {css}\n        clip end in seconds, e.g. 4008 (1h, 6m, 48s -> 4008s)\n      {ce}\n        clip end as per [(h*)mm]ss, e.g. 10703 (1h, 07m, 03s)\n      {ces}\n        clip end in seconds, e.g. 4023 (1h, 07m, 03s -> 4023s)\n      {cer}\n        e.g. +15\n    \n      notes:\n        1. pymtheg placeholders can only be used with `-tf, --timestamp-format`\n        2. "[(h*)mm]ss": seconds and minutes will always be represented as 2\n           digits and will be right adjusted with 0s if needed, however hours\n           can be represented by any number of characters, e.g. "1" or "123456"\n```\n\n### Examples\n\n1. Get a song through a Spotify link\n\n   ```text\n   pymtheg "https://open.spotify.com/track/7CH99b2i1TXS5P8UUyWtnM"\n   ```\n\n2. Get a song through a search query\n\n   ```text\n   pymtheg "thundercat - them changes"\n   ```\n\n3. Get multiple songs through multiple queries\n\n   ```text\n   pymtheg "https://open.spotify.com/track/7CH99b2i1TXS5P8UUyWtnM" "silk sonic blast off"\n   ```\n\n4. Same as 1, however you set the clip start to random and let pymtheg suprise you\n\n   ```text\n   pymtheg "https://open.spotify.com/track/7CH99b2i1TXS5P8UUyWtnM" -cs "*" -ce "+15" --use-defaults\n   ```\n\n## License\n\npymtheg is unlicensed with The Unlicense. In short, do whatever. You can find copies of\nthe license in the\n[UNLICENSE](https://github.com/markjoshwel/pymtheg/blob/main/UNLICENSE) file or in the\n[pymtheg module docstring](https://github.com/markjoshwel/pymtheg/blob/main/pymtheg.py#L5).\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/markjoshwel/pymtheg',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
