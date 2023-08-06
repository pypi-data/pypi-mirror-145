# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nbswave']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.5,<2.0.0', 'pydub>=0.25.1,<0.26.0', 'pynbs>=0.4.2,<0.5.0']

setup_kwargs = {
    'name': 'nbswave',
    'version': '0.2.0',
    'description': 'An utility to render note block songs to a variety of audio formats',
    'long_description': '# nbswave\n\nA Python package to render note block songs to a variety of audio formats.\n\n## Overview\n\nnbswave is a Python package aimed at rendering note block songs from [Open Note Block Studio](https://opennbs.org/) to audio tracks. Supports many common audio formats, both for loading custom sounds as well as exporting tracks.\n\n## Setup\n\nThe package can be installed with `pip`.\n\n```shell\n$ pip install nbswave\n```\n\nIn order to use the package, [FFmpeg](https://www.ffmpeg.org/) must be available:\n\n1. Download precompiled binaries for `ffmpeg` and `ffprobe` [here](https://ffbinaries.com/downloads).\n2. Add the destination folder to your `PATH`, or, alternatively, place both executables in the root folder of the project.\n\n## Usage\n\n```python\nfrom nbswave import *\n\nrender_audio("song.nbs", "output.mp3")\n```\n\nThe output format will be detected automatically based on the file extension. You can still specify it explicitly if you\'d like:\n\n```python\nfrom nbswave import *\n\nrender_audio("song.nbs", "output", format=\'wav\')\n```\n\n> Compatibility with audio formats depends on your FFmpeg configuration.\n\n### Custom instruments\n\nIn order to render songs with custom instruments, you have a few options:\n\n1. Copy the sounds manually to the `sounds` folder\n\n2. Pass the path to a folder (or ZIP file) containing custom sounds:\n\n```python\nfrom pathlib import Path\n\nnbs_sounds_folder = Path.home() / "Minecraft Note Block Studio" / "Data" / "Sounds"\nrender_audio("song.nbs", "output.mp3", custom_sound_path=nbs_sounds_folder)\n```\n\nIf any sound file used in the song is not found in that location, a `MissingInstrumentException` will be raised. This behavior can be suppressed with the following argument:\n\n```python\nrender_audio("song.nbs", "output.mp3", ignore_missing_instruments=True)\n```\n\n### Advanced usage\n\nFor more advanced use cases where you might need more control over the export process, it\'s possible to use the `SongRenderer` class. This will allow you to load custom instruments from multiple sources, as well as query which instruments are still missing:\n\n```python\nfrom nbswave import *\n\nrenderer = SongRenderer("song.nbs")\n\nrenderer.load_instruments(nbs_sounds_folder)\nrenderer.load_instruments("some_more_instruments.zip")\n\nrenderer.missing_instruments()\n\nrenderer.mix_song()\n```\n\n## Contributing\n\nContributions are welcome! Make sure to open an issue discussing the problem or feature suggestion before creating a pull request.\n\nThis project uses [poetry](https://python-poetry.org/) for managing dependencies. Make sure to install it, and run:\n\n```shell\n$ poetry install\n```\n\nThis project follows the [black](https://github.com/psf/black) code style. Import statements are sorted with [isort](https://pycqa.github.io/isort/).\n\n```shell\n$ poetry run isort nbswave\n$ poetry run black nbswave\n$ poetry run black --check nbswave\n```\n\n---\n\nLicense - [MIT](https://github.com/Bentroen/nbswave/blob/main/LICENSE)\n',
    'author': 'Bentroen',
    'author_email': 'bemcdc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Bentroen/nbswave',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
