# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['szurubooru_toolkit', 'szurubooru_toolkit.scripts']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.4.0,<9.0.0',
 'Pybooru>=4.2.2,<5.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'keras>=2.8.0,<3.0.0',
 'loguru>=0.6.0,<0.7.0',
 'numpy>=1.22.1,<2.0.0',
 'pathvalidate>=2.5.0,<3.0.0',
 'pygelbooru>=0.3.2,<0.4.0',
 'pysaucenao>=1.6.1,<2.0.0',
 'pyszuru>=0.2.4,<0.3.0',
 'requests>=2.25.1,<3.0.0',
 'syncer>=1.3.0,<2.0.0',
 'tensorflow>=2.8.0,<3.0.0',
 'tomlkit>=0.10.0,<0.11.0',
 'tqdm>=4.59.0,<5.0.0',
 'validators>=0.18.2,<0.19.0']

entry_points = \
{'console_scripts': ['auto-tagger = '
                     'szurubooru_toolkit.scripts.auto_tagger:main',
                     'create-tags = '
                     'szurubooru_toolkit.scripts.create_tags:main',
                     'upload-media = '
                     'szurubooru_toolkit.scripts.upload_media:main']}

setup_kwargs = {
    'name': 'szurubooru-toolkit',
    'version': '0.4.0',
    'description': 'Python package and script collection to manage szurubooru.',
    'long_description': '<p align="center">\n<img src="https://cdn-icons-png.flaticon.com/512/2581/2581053.png"\n  alt="szurubooru-toolkit icon"\n  width="128" height="128">\n</p>\n\n# szurubooru-toolkit\nPython package and script collection to manage your [szurubooru](https://github.com/rr-/szurubooru) image board.\n\n## Requirements\nIn order to run the included scripts, a Python release `>=3.8` and the configuratrion file `config.toml` is required.\n\nThe `config.toml` file needs to be present in your current working directory.\nYou can find a sample config file in the [git repository](https://github.com/reluce/szurubooru-toolkit) of this package.\n\n## Installation\nThis package is available on [PyPI](https://pypi.org/project/szurubooru-toolkit/) and can be installed with pip:\n`pip install szurubooru-toolkit`\n\nAlternatively, you can clone the package from GitHub and set everything up with [Poetry](https://python-poetry.org/docs/). In the root directory of this repository, execute `poetry install`.\n\nPlease note this package requires Tensorflow for Deepbooru tagging and other required packages which do take up quite a lot of disk space (>400MB).\nA future release of this package will offer an option without the need to install Tensorflow if you don\'t want to use Deepbooru tagging.\n\n## User configuration\nMake your changes in the `config_sample.toml` file provided in the git repo and rename it to `config.toml` afterwards.\n\nNote that path names have to be specified with forward slashes (/) if you\'re using Windows.\n\n<details>\n  <summary>config.toml reference</summary>\n\n| Section | Option | Description | Examples/Default |\n|---------|--------|-------------|-----------------|\n| szurubooru | url | The URL of your szurubooru | `"https://szuru.example.com"` |\n| szurubooru | username | Username which connects to the szuruboori API | `"my_szuru_user"` |\n| szurubooru | api_token | API token of `username`. Generate one in szurubooru from _Account_ > _Login tokens_ > _Create token_ | `"my_api_token"` |\n| szurubooru | public | If your szurubooru is reachable over the internet | `false` |\n| auto_tagger | saucenao_api_token | In case you want to increase your daily query limit | `"my_saucenao_api_token"` |\n| auto_tagger | saucenao_enabled | Set this to `false` and `deepbooru_enabled` to `true` if you only want to tag with Deepbooru | `true` |\n| auto_tagger | deepbooru_enabled | If enabled, tag the post with Deepbooru if no tags with SauceNAO were found | `false` |\n| auto_tagger | deepbooru_model | Path to the Deepbooru model | `"./misc/deepbooru/model-resnet_custom_v3.h5"` |\n| auto_tagger | deepbooru_threshold | Define how accurate the matched tag from Deepbooru has to be | `"0.7"` |\n| auto_tagger | deepbooru_forced | Always tag with SauceNAO and Deepbooru | `false` |\n| auto_tagger | hide_progress | Set this to true to hide the progress bar | `false` |\n| auto_tagger | tmp_path | Local path where media files get downloaded temporarily if you szurubooru is not public. | `/tmp`, `C:/Users/Foo/Desktop` |\n| danbooru | user | Danbooru user | `"None"` |\n| danbooru | api_key | Danbooru api key | `"None"` |\n| gelbooru | user | Gelbooru user | `"None"` |\n| gelbooru | api_ley | Gelbooru api key | `"None"` |\n| konachan | user | Konachan user | `"None"` |\n| konachan | password | Konachan password | `"None"` |\n| yandere | user | Yandere user | `"None"` |\n| yandere | password | Yandere password | `"None"` |\n| pixiv | user | Pixiv user. Currently not being used. | `"None"` |\n| pixiv | password | Pixiv password. Currently not being used. | `"None"` |\n| pixiv | token | Pixiv token. Currently not being used. | `"None"` |\n| upload_media | src_path | Every valid media file under this dir (recursively) will get uploaded | `"/local/path/to/upload/dir"` |\n| upload_media | hide_progress | Set this to true to hide the progress bar | `false` |\n| upload_media | cleanup | Set this to true if images in the `src_path` should be deleted after upload | `false` |\n| upload_media | tags | These tags will get set for all uploaded posts. Separate them by a comma. | `["tagme", "tag1", "tag2", "tagN"]` |\n| upload_media | auto_tag | Set this to true if you want your post to be automatically tagged after upload | `false` |\n| logging | log_enabled | If logging to a log file should be enabled | `false` |\n| logging | log_file | Specify the path of the log file | `"C:/Users/Foo/Desktop/szurubooru_toolkit.log"` |\n| logging | log_level | Specify the log level. `DEBUG` logs the most information | `"DEBUG"\\|"INFO"\\|"WARNING"\\|"ERROR"\\|"CRITICAL"` |\n| logging | log_colorized | If the log file should be colorized. Requires compatible viewer (e.g. `less -r <log_file>`). | `true` |\n</details>\n\nCreating a SauceNAO account and an API key is recommended.\nPlease consider supporting the SauceNAO team as well by upgrading your plan.\nWith a free plan, you can request up to 200 posts in 24h.\n\nFor Deepbooru support, download the current release [here](https://github.com/KichangKim/DeepDanbooru/releases/tag/v3-20211112-sgd-e28) (v3-20211112-sgd-e28) and extract the contents of the zip file. Specify the path of the folder with the extracted files in `deepbooru_model`.\nPlease note that you have to set `deepbooru_enabled` if you want to use it.\n\n## Scripts\n\n### auto-tagger\nThis script accepts a szurubooru query as a user input, fetches all posts returned by it and attempts to tag it using SauceNAO/Deepbooru.\n\nIf no matches from SauceNAO were found, the script keeps the previously set tags of the post and additionally appends the tag `tagme`.\n\nYou can set `deepbooru_enabled` to `true` in your config.toml file. In that case, the script falls back to tag posts with the supplied Deepbooru model.\nIf you only want to use Deepbooru, set `deepbooru_enabled` to `true` and `saucenao_enabled` to `false`. If you want to use SauceNAO and Deepbooru, set following options to `true`: `saucenao_enabled`, `deepbooru_enabled` and `deepbooru_forced`.\n\n__Usage__\n\nAfter editing and renaming the sample config file to config.toml, we can just execute the script with our query:\n\n* `auto-tagger "date:today tag-count:0"`\n* `auto-tagger "date:2021-04-07"`\n* `auto-tagger "tagme"`\n* `auto-tagger "id:100,101"`\n\nIf we want to tag a single post, we can omit the keyword `id` in our query:\n\n* `auto-tagger 100`\n\nAlternatively, we can tag a single post and specify `--sankaku_url` to fetch the tags from the supplied URL (_untested with current release_):\n\n`auto-tagger --sankaku_url https://chan.sankakucomplex.com/post/show/<id> 100`\n\nThis is especially useful since Sankaku has changed their API and aggregator sites like SauceNAO don\'t have the latest results there.\n\nIf you cloned the repo from GitHub, prefix the above commands with `poetry run`, e.g. `poetry run auto-tagger "date:today"`. Note that your current working directory has to be the the root of the GitHub project.\n\n### upload-media\nThis script searches through your specified upload folder in the config file for any image/video files and uploads them to your szurubooru.\n\n__Usage__\n\nAfter editing the config file, we can just execute the script.\n\nIf you installed it with pip, execute `upload-media`. Note that `config.toml` has to be in your current working directory.\n\nIf you cloned the repo from GitHub, execute `poetry run upload-media`. Note that your current working directory has to be the the root of the GitHub project.\n\n### create-tags (Currently not working, WIP)\nThis script reads the file `./misc/tags/tags.txt`, parses its contents and creates the tags in your szurubooru.\n\nIf the tag already exists, it will get updated with your changes.\n\nYou can use tools like [Grabber](https://github.com/Bionus/imgbrd-grabber) to download a tag list from common boorus.\n\nThe file has to be in following format:\n\n```\n<tag_a>,<category_number>\n<tag_b>,<category_number>\n<tag_..n>,<category_number>\n```\n\n|Category|Number|\n|---|---|\n|default|0|\n|artist|1|\n|series|2|\n|character|3|\n|meta|4|\n\n__Usage__\n\nAfter editing the config file, we can just execute the script.\n\nIf you installed it with pip, execute `create-tags`. Note that `config.toml` has to be in your current working directory.\n\nIf you cloned the repo from GitHub, execute `poetry run create-tags`. Note that your current working directory has to be the the root of the GitHub project.\n\n## Image credit\nGitHub repo icon: <a href="https://www.flaticon.com/free-icons/code" title="code icons">Code icons created by Smashicons - Flaticon</a>\n',
    'author': 'reluce',
    'author_email': 'reluce@fkosquad.moe',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/reluce/szurubooru-toolkit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
