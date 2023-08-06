# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tootbot']

package_data = \
{'': ['*']}

install_requires = \
['Mastodon.py>=1.5.1,<2.0.0',
 'Pillow>=9.0.1,<10.0.0',
 'about-time>=3.1.1,<4.0.0',
 'alive-progress>=2.3.1,<3.0.0',
 'arrow>=1.2.2,<2.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'elapsed>=2020.12.3,<2021.0.0',
 'gfycat>=0.2.2,<0.3.0',
 'httpx>=0.22.0,<0.23.0',
 'imgurpython>=1.1.7,<2.0.0',
 'praw>=7.5.0,<8.0.0',
 'rich>=12.0.0,<13.0.0']

entry_points = \
{'console_scripts': ['tootbot = tootbot.command_line:start',
                     'tootbot_create_config = tootbot.create_config:create']}

setup_kwargs = {
    'name': 'tootbot',
    'version': '4.0.0',
    'description': 'A Python bot that looks up posts from specified subreddits and automatically posts them on Mastodon',
    'long_description': "# Tootbot\n\nThis is a Python bot that looks up posts from specified subreddits and automatically posts them on [Mastodon][1].\nIt is based on [reddit-twitter-bot][2].\n\n---\n\n**!!! This version of Tootbot no longer supports posting to Twitter. !!!**\nIf you need twitter functionality look into [reddit-twitter-bot][2] as a possible alternative.\n\n**!!! This version of Tootbot no longer supports deleting old toots. !!!**\nIf you'd like to delete older toots from your Mastodon account look into [MastodonAmnesia][3] as a tool that might\nwork for you.\n\n\n---\n\n**Features:**\n\n* Tootbot posts to [Mastodon][1]\n* Media from direct links, Gfycat, Imgur, Reddit, and Giphy is automatically attached in the social media post.\n  Tootbot attaches up to the first 4 pictures for imgur albums and reddit gallery posts.\n* Links that do not contain media can be skipped, ideal for meme accounts like [@babyelephantgifs][4]\n* NSFW content, spoilers, and self-posts can be filtered\n* Tootbot can monitor multiple subreddits at once\n* Tootbot is fully open-source, so you don't have to give an external service full access to your social media accounts\n* Tootbot also checks the sha256 checksum of media files to stop posting of the same media file from different subreddits.\n* Tootbot can ping a [Healthchecks][5] instance for monitoring continuous operation of Tootbot\n* Optionally throttle down frequency of tooting when mastodon errors are detected.\n\n## Disclaimer\n\nThe developers of Tootbot hold no liability for what you do with this script or what happens to you by using this\nscript. Abusing this script *can* get you banned from Mastodon, so make sure to read up on proper usage of the API\nfor each site.\n\n## Setup and usage\n\nFor instructions on setting up and using Tootbot, please visit [the wiki][6]\n\n## Supporting Tootbot\n\nThere are a number of ways you can support Tootbot:\n\n- Create an issue with problems or ideas you have with/for Tootboot\n- You can [buy me a coffee][7].\n- You can send me small change in Monero to the address below:\n\nMonero donation address:\n`87C65WhSDMhg4GfCBoiy861XTB6DL2MwHT3SWudhjR3LMeGEJG8zeZZ9y4Exrtx5ihavXyfSEschtH4JqHFQS2k1Hmn2Lkt`\n\n[1]: https://joinmastodon.org/\n[2]: https://github.com/rhiever/reddit-twitter-bot\n[3]: https://pypi.org/project/mastodonamnesia/\n[4]: https://botsin.space/@babyelephantgifs\n[5]: https://healthchecks.io/\n[6]: https://codeberg.org/MarvinsMastodonTools/tootbot/wiki\n[7]: https://www.buymeacoffee.com/marvin8\n",
    'author': 'marvin8',
    'author_email': 'marvin8@tuta.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://codeberg.org/MarvinsMastodonTools/tootbot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
