# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyhifiberry',
 'pyhifiberry.engineio_v4',
 'pyhifiberry.engineio_v4.async_drivers',
 'pyhifiberry.socketio_v5']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'bidict>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'pyhifiberry',
    'version': '0.1.1',
    'description': 'Python library to interface with Hifiberry OS API.',
    'long_description': "# pyhifiberry\nPython library to interface with Hifiberry OS API (audiocontrol2). There are two APIs available:\n* [REST](https://github.com/hifiberry/audiocontrol2/blob/master/doc/api.md)\n* [socketio](https://github.com/hifiberry/audiocontrol2/blob/master/doc/socketio_api.md)\n\nThis package is targeting mainly the needs for a [hifiberry integration for Home assistant](https://github.com/willholdoway/hifiberry).\n\n## Usage example of the socketio API\nRuns for 100 secs and prints artist name if metadata events occure.\n``` python\nimport asyncio\nfrom pyhifiberry.audiocontrol2sio import Audiocontrol2SIO\n\ndef metadata_callback(metadata):\n    print(metadata['artist'])\n\nasync def main():\n    api = await Audiocontrol2SIO.connect(<HIFIBERRY_IP>, <HIFIBERRY_PORT>)\n    api.metadata.add_callback(metadata_callback)\n    await asyncio.sleep(100)\n\nif __name__ == '__main__':\n    asyncio.run(main())\n```",
    'author': 'Diogo Gomes',
    'author_email': 'diogogomes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/schnabel/pyhifiberry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
