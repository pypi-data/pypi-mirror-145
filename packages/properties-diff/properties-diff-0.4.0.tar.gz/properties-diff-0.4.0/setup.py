# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['properties_diff']

package_data = \
{'': ['*']}

install_requires = \
['colorama']

entry_points = \
{'console_scripts': ['properties-diff = properties_diff.diff:run',
                     'properties-patch = properties_diff.patch:run']}

setup_kwargs = {
    'name': 'properties-diff',
    'version': '0.4.0',
    'description': 'Command line tool to compare properties files',
    'long_description': '![Github](https://img.shields.io/github/tag/essembeh/properties-diff.svg)\n![PyPi](https://img.shields.io/pypi/v/properties-diff.svg)\n![Python](https://img.shields.io/pypi/pyversions/properties-diff.svg)\n![](https://github.com/essembeh/properties-diff/actions/workflows/poetry.yml/badge.svg)\n\n\n# properties-diff\n\n`properties-diff` is a command line tools to compare *properties* files and print differences with colors as if you were using `wdiff` or `diff` tools.\n\nEven if *properties* files are text files, using directly `diff` is not that efficient because of key/value pairs order or format (for example using `=` or `[space]=[space]` as separator, double quoting values...). `properties-diff` compare key/value pairs but not the order nor the format.\n\n`properties-patch` is a command line tools to patch a *properties* files with one or more *properties* files to add, update or delete some properties.\n\n\n\n# Install\n\nInstall the latest release from [PyPI](https://pypi.org/project/properties-diff/)\n```sh\n$ pip3 install properties-diff\n$ properties-diff path/to/file.properties path/to/another/file.properties\n```\n\nInstall from the sources\n```sh\n$ pip3 install --user --upgrade git+https://github.com/essembeh/properties-diff\n$ properties-diff path/to/file.properties path/to/another/file.properties\n```\n\n\n# Usage\n\n```sh\n$ properties-diff --help                                                                                                                               130\nusage: properties-diff [-h] [-q] [--quote] [--sep SEP] [-m {simple,diff,wdiff}] [-A] [-D] [-U] left.properties right.properties\n\npositional arguments:\n  left.properties       left file to compare\n  right.properties      right file to compare\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -q, --quiet           print less information\n  --quote               use double quotes for values, example: foo="bar"\n  --sep SEP             key/value separator, default is \'=\'\n  -m {simple,diff,wdiff}, --mode {simple,diff,wdiff}\n                        select a format to show differences: using colors only (simple), using diff-like format (diff) or wdiff-like (wdiff) format. Default is \'wdiff\'\n  -A, --added           print added properties\n  -D, --deleted         print deleted properties\n  -U, --updated         print updated properties\n\n```\n\n\n```sh\n$ properties-patch --help\nusage: properties-patch [-h] [-c] [--comments] [-f] [-i] [--quote] [--sep SEP] [-A] [-D] [-U] -p patch.properties [-o output.properties] source.properties\n\npositional arguments:\n  source.properties     file to modify\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -c, --color           print colors\n  --comments            insert comment when property is added, updated or deleted\n  -f, --force           force output file (--output) overwrite if it already exists\n  -i, --interactive     ask for confirmation to add, update or delete a property\n  --quote               use double quotes for values, example: foo="bar"\n  --sep SEP             key/value separator, default is \'=\'\n  -p patch.properties, --patch patch.properties\n                        patch file\n  -o output.properties, --output output.properties\n                        modified file\n\n  -A, --add             add new properties from patches\n  -D, --delete          delete properties not in patches\n  -U, --update          update properties from patches\n\n```\n\n\n## properties-diff modes\n\nYou can see differences between the properties files using 3 modes using `--mode <MODE>` or `-m <MODE>`\n* `wdiff`, prints the changes like `wdiff` tool would do (this is the default mode)\n* `diff`, prints the changes like `diff` tool would do\n* `simple`, based on colors, *red* for removed lines, *green* for added lines\n\n![wdiff](images/wdiff.png)\n![diff](images/diff.png)\n![simple](images/simple.png)\n',
    'author': 'Sébastien MB',
    'author_email': 'seb@essembeh.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/essembeh/properties-diff',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
