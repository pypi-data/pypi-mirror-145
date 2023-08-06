# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.captions']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0', 'pelican>=4.5,<5.0']

extras_require = \
{'markdown': ['markdown>=3.2.2,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-captions',
    'version': '0.4.0',
    'description': 'Add captions and labels to figures, tables and code blocks.',
    'long_description': '# captions: A Plugin for Pelican\n\n[![Build Status](https://img.shields.io/github/workflow/status/f-koehler/pelican-captions/build)](https://github.com/f-koehler/pelican-captions/actions)\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-captions)](https://pypi.org/project/pelican-captions/)\n![License](https://img.shields.io/pypi/l/pelican-captions?color=blue)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/f-koehler/pelican-captions/main.svg)](https://results.pre-commit.ci/latest/github/f-koehler/pelican-captions/main)\n\nEncapsulate standalone images in a figure tag and add a figcaption tag.\n\n## Installation\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-figures\n\n## Usage\n\n<<Add plugin details here>>\n\n## Contributing\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/f-koehler/pelican-captions/issues\n[contributing to pelican]: https://docs.getpelican.com/en/latest/contribute.html\n\n## License\n\nThis project is licensed under the AGPL-3.0 license.\n',
    'author': 'Fabian Köhler',
    'author_email': 'fabian.koehler@protonmail.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/f-koehler/pelican-captions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
