# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypers']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.1,<10.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'dnspython>=2.2.0,<3.0.0',
 'httpx>=0.22.0,<0.23.0',
 'motor>=2.5.1,<3.0.0']

setup_kwargs = {
    'name': 'pypers',
    'version': '1.1.0',
    'description': 'A utilities module made for personal use, has small snippets which I use in many projects.',
    'long_description': '# pypers\n\n<p align="center">\n    <a href="https://pypers.divkix.me"><img src="img/name.png"></a>\n    </br></br>\n    <a href="https://pypi.org/project/PyPers/"><img src="https://img.shields.io/pypi/v/PyPers" alt="PyPI"></a>\n    <a href="https://github.com/Divkix/PyPers/actions"><img src="https://github.com/Divkix/PyPers/workflows/CI%20%28pip%29/badge.svg" alt="CI (pip)"></a>\n    <a href="https://pypi.org/project/pypers/"><img src="https://img.shields.io/pypi/wheel/PyPers.svg" alt="PyPI - Wheel"></a>\n    <a href="https://pypi.org/project/pypers/"><img src="https://img.shields.io/pypi/pyversions/PyPers.svg" alt="Supported Python Versions"></a>\n    <a href="https://pepy.tech/project/PyPers"><img src="https://pepy.tech/badge/PyPers" alt="Downloads"></a>\n</p>\n\nPackage with helper scripts.\n\nContains some helper function which make up its name: python+helpers = pypers.\n\n\n## Usage:\n\n### pypers.mongo_helpers:\n```python\nfrom pypers.mongo_helpers import AsyncMongoDB\n\ndb = AsyncMongoDB(\'localhost:27017\', \'pypers\')\ndb.collection = "test"\n\nawait db.insert_one({\'name\': \'pypers\'})\nresults = await db.find_one({\'name\': \'pypers\'})\nprint(results)\nawait db.delete_one({\'name\': \'pypers\'})\n```\n\n\n### pypers.namespace:\n```python\nfrom pypers.namespace import Namespace\n\nns = Namespace(\n    a=1,\n    b=2,\n    c=Namespace(\n        d=3,\n        e=4,\n    ),\n)\n\nprint(ns.a)\nprint(ns.b)\nprint(ns.c.d)\nprint(ns.c.e)\n```\n\n### pypers.url_helpers:\n```python\nfrom pypers.url_helpers import UrlHelpers\nfrom pypers.url_helpers import AioHttp\n\nnew_url = await UrlHelpers.shorten_url(\'https://www.google.com\')\nprint(new_url)\n\njson, resp = AioHttp.get_json(\'https://www.google.com\')\nprint(json, resp)\n\ntext, resp = AioHttp.get_text(\'https://www.google.com\')\nprint(text, resp)\n\nraw, resp = AioHttp.get_raw(\'https://www.google.com\')\nprint(raw, resp)\n\njson, resp = AioHttp.post_json(\'https://www.google.com\')\nprint(json, resp)\n```\n\n### pypers.image_tools:\n\n```python\nfrom pypers.image_tools import ImageTools\n\nnew_img = ImageTools.compress_image(\'/path/to/image.jpg\', quality=50)\nprint(new_img)\n```\n\n### pypers.formatters:\n\n```python\nfrom pypers.formatters import Formatters\n\nhumanbytes_size = Formatters.humanbytes(1024*1024)\nprint(humanbytes_size)\n\nhuman_time = Formatters.time_formatter(15000)\nprint(human_time)\n```\n',
    'author': 'Divkix',
    'author_email': 'techdroidroot@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypers.divkix.me',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
