# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.references', 'pelican.plugins.references.labels']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'pelican>=4.5',
 'pre-commit>=2.13.0,<3.0.0',
 'pybtex>=0.24.0,<0.25.0']

extras_require = \
{'markdown': ['markdown>=3.2']}

entry_points = \
{'pybtex.style.labels': ['pybtex.style.labels.number_brackets = '
                         'pelican.plugins.references.labels.number_brackets:LabelStyle']}

setup_kwargs = {
    'name': 'pelican-references',
    'version': '0.3.0',
    'description': 'Generate bibliographies from BibTeX files',
    'long_description': '# references: A Plugin for Pelican\n\n[![Build Status](https://img.shields.io/github/workflow/status/f-koehler/pelican-references/build)](https://github.com/f-koehler/pelican-references/actions)\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-references)](https://pypi.org/project/pelican-references/)\n![License](https://img.shields.io/pypi/l/pelican-references?color=blue)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/f-koehler/pelican-references/main.svg)](https://results.pre-commit.ci/latest/github/f-koehler/pelican-references/main)\n\nGenerate bibliographies from BibTeX files\n\n## Installation\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-references\n\n## Usage\n\n<<Add plugin details here>>\n\n## Contributing\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/f-koehler/pelican-references/issues\n[contributing to pelican]: https://docs.getpelican.com/en/latest/contribute.html\n\n## License\n\nThis project is licensed under the AGPL-3.0 license.\n',
    'author': 'Fabian Köhler',
    'author_email': 'fabian.koehler@protonmail.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/f-koehler/pelican-references',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
