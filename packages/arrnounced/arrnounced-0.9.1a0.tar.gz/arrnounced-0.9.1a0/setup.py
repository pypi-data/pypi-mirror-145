# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arrnounced']

package_data = \
{'': ['*'],
 'arrnounced': ['templates/*',
                'templates/assets/bootstrap/css/*',
                'templates/assets/bootstrap/fonts/*',
                'templates/assets/bootstrap/js/*',
                'templates/assets/css/*',
                'templates/assets/js/*']}

install_requires = \
['Flask-Login==0.4.1',
 'Flask-SocketIO>=4.3.2,<5.0.0',
 'Flask==1.1.1',
 'aiohttp==3.8.1',
 'defusedxml==0.6.0',
 'pony==0.7.14',
 'pydle==0.9.4',
 'tomlkit==0.7.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['arrnounced = arrnounced.cli:main']}

setup_kwargs = {
    'name': 'arrnounced',
    'version': '0.9.1a0',
    'description': 'Notify Sonarr/Radarr/Lidarr of tracker IRC announcements',
    'long_description': '# Arrnounced\nNotify Sonarr/Radarr/Lidarr of tracker IRC announcements.\n\nBuilt on the work of\n[sonarrAnnounced](https://github.com/l3uddz/sonarrAnnounced) with tracker\nconfiguration from\n[autodl-trackers](https://github.com/autodl-community/autodl-trackers) (used by\n[autodl-irssi](https://github.com/autodl-community/autodl-irssi))\n\n## Features\n* All trackers from\n[autodl-trackers](https://github.com/autodl-community/autodl-trackers/tree/master/trackers)\nare supported.\n* Web UI to list announcements and accepted notifications\n    * Ability to search among the announcements remains to be implemented though\n* Notify based on announcement category\n* Configurable delay between IRC announcement and notification\n\nOnly a few of the supported trackers are tested at the moment. Please report any issues you find.\n\n## Screenshots\n\n### Main page\n![Index Page](https://raw.githubusercontent.com/weannounce/arrnounced/img/doc/index.PNG)\n### Status page\n![Status Page](https://raw.githubusercontent.com/weannounce/arrnounced/img/doc/status.gif)\n\n# Setup\n\n_Release v0.7 updated the configuration format. See the [release\nnotes](https://github.com/weannounce/arrnounced/releases/tag/v0.7) for more\ninformation._\n\n## Configuration\nThe default configuration path is `~/.arrnounced/settings.toml`.\n[example.cfg](https://github.com/weannounce/arrnounced/blob/master/example.cfg)\nis the acting configuration documentation.\n\nThe default XML tracker configuration path is `~/.arrnounced/autodl-trackers/trackers`\n\n## Installation\n\n```bash\n# Optional virtual environment\n$ python -m venv path/to/venv\n$ source path/to/venv/bin/activate\n\n# Install\n$ pip install arrnounced\n\n# Run\n$ arrnounced\n```\n\nConfiguration files path as well as log and database location may be changed with command line arguments.\n\n\n### Docker\n[Arrnounced on dockerhub](https://hub.docker.com/r/weannounce/arrnounced)\n\n* You must provide `settings.toml` in `/config`. This is also where logs and the database will be stored.\n* To access the web UI using bridged network the webui host in settings.toml must be `0.0.0.0`.\n* As Arrnounced runs as a non-root user by default it is recommended to specify your own user to handle write access to `/config`.\n\n```bash\n# Default example\ndocker run -v /path/to/settings:/config \\\n           --user 1000 \\\n           -p 3467:3467 weannounce/arrnounced:latest\n```\n\nThe docker image comes with a snapshot of XML tracker configurations located under `/trackers`. If you prefer your own version you can mount over it.\n\n```bash\n# Example with custom XML tracker configs and verbose logging\ndocker run -v /path/to/settings:/config \\\n           -v /path/to/autodl-trackers/trackers:/trackers \\\n           -e VERBOSE=Y \\\n           --user 1000 \\\n           -p 3467:3467 weannounce/arrnounced:latest\n```\n\n## Database design update\nThe database design was updated in [v0.3](https://github.com/weannounce/arrnounced/releases/tag/v0.3)\n([ef931ee](https://github.com/weannounce/arrnounced/commit/ef931eef27348f82254d601f96d094a7b9f147bb)).\nIf you used Arrnounced prior to this or used its predecessor you have two options.\n* Convert your old database using [convert_db.py](https://github.com/weannounce/arrnounced/blob/master/convert_db.py)\n* Move the old database file for safe keeping and let Arrnounced create a new file.\n\nThe default path to the database is `~/.arrnounced/brain.db`\n',
    'author': 'WeAnnounce',
    'author_email': 'weannounce@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/weannounce/arrnounced',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
