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
    'version': '2.2.0',
    'description': 'A Python script to share songs from Spotify/YouTube as a 15 second clip.',
    'long_description': '# pymtheg\n\nA Python script to share songs from Spotify/YouTube as a 15 second clip.\n[Designed for use with Termux.](https://github.com/markjoshwel/pymtheg/blob/main/TERMUX.md)\n\nSee the [repository](https://github.com/markjoshwel/pymtheg) for more installation and\ncontribution instructions/information.\n\n[![asciicast](https://asciinema.org/a/483803.svg)](https://asciinema.org/a/483803)\n\n## Installation\n\npymtheg requires [Python 3.6.2](https://python.org/) or later, and\n[ffmpeg](https://ffmpeg.org/).\n\n## Usage\n\n```text\nusage: pymtheg [-h] [-d DIR] [-o OUT] [-sda SDARGS] [-ffa FFARGS] [-cs CLIP_START] [-ce CLIP_END] [-i IMAGE] [-ud] [-y] query\n\na python script to share songs from Spotify/YouTube as a 15 second clip\n\npositional arguments:\n  query                 song/link from spotify/youtube\n\noptions:\n  -h, --help            show this help message and exit\n  -d DIR, --dir DIR     directory to output to\n  -o OUT, --out OUT     output file path, overrides directory arg\n  -sda SDARGS, --sdargs SDARGS\n                        args to pass to spotdl\n  -ffa FFARGS, --ffargs FFARGS\n                        args to pass to ffmpeg for clip creation\n  -cs CLIP_START, --clip-start CLIP_START\n                        specify clip start (default 0)\n  -ce CLIP_END, --clip-end CLIP_END\n                        specify clip end (default +15)\n  -i IMAGE, --image IMAGE\n                        specify custom image\n  -ud, --use-defaults   use 0 as clip start and --clip-length as clip end\n  -y, --yes             say yes to every y/n prompt\n\nffargs default: "-hide_banner -loglevel error -c:a aac -c:v libx264 -pix_fmt yuv420p -tune stillimage -vf scale=\'iw+mod(iw,2):ih+mod(ih,2):flags=neighbor\'"\n```\n\n## License\n\npymtheg is unlicensed with The Unlicense. In short, do whatever. You can find copies of\nthe license in the\n[UNLICENSE](https://github.com/markjoshwel/pymtheg/blob/main/UNLICENSE) file or in the\n[pymtheg module docstring](https://github.com/markjoshwel/pymtheg/blob/main/pymtheg.py#L5).\n',
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
