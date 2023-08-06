# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cda_downloader',
 'cda_downloader.cda',
 'cda_downloader.common',
 'cda_downloader.downloader']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4,<5', 'click>=8.1.2,<9.0.0', 'requests>=2.27,<3.0']

setup_kwargs = {
    'name': 'cda-downloader',
    'version': '0.1.0',
    'description': 'CDA.PL Video downloader',
    'long_description': '# CDA Downloader\n\n## Getting Started\n\n`pip install cda_downloader`\n\n## Basic usage\n\nImport CDA class from the package\n\n```\nfrom cda_downloader import CDA:\n```\n\nCreate an instance. You can specify number of thread, api usage and progress bar:\n\n```\ncda = CDA(multithreading=0, use_api=True, progress_bar=True)\n```\n\nTo download video use `download_video` method. You can provide string or Iterable of strings:\n\n```\ncda.download_videos(path="/download", urls="https://www.cda.pl/video/13617843")\ncda.download_videos(path="/download", urls=("https://www.cda.pl/video/13617843",))\n```\n\nYou can also use `get_video_urls` method instead to get uls without a download:\n\n```\ncda.get_video_urls(path="/download", urls="https://www.cda.pl/video/13617843")\ncda.get_video_urls(path="/download", urls=("https://www.cda.pl/video/13617843",))\n```',
    'author': 'sovereign527',
    'author_email': 'sovereign527@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sovereign527/cda_downloader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0.0',
}


setup(**setup_kwargs)
