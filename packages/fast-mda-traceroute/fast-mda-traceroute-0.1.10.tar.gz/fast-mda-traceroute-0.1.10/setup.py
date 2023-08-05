# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_mda_traceroute',
 'fast_mda_traceroute.algorithms',
 'fast_mda_traceroute.formats']

package_data = \
{'': ['*']}

install_requires = \
['diamond-miner>=0.9.1,<0.10.0',
 'more-itertools>=8.12.0,<9.0.0',
 'pycaracal>=0.8.1,<0.9.0',
 'tabulate>=0.8.9,<0.9.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['fast-mda-traceroute = fast_mda_traceroute.cli:app']}

setup_kwargs = {
    'name': 'fast-mda-traceroute',
    'version': '0.1.10',
    'description': 'An experimental multipath traceroute tool.',
    'long_description': '# fast-mda-traceroute\n\n[![Coverage][coverage-badge]][coverage-url]\n[![Docker Status][docker-workflow-badge]][docker-workflow-url]\n[![PyPI Status][pypi-workflow-badge]][pypi-workflow-url]\n[![Tests Status][tests-workflow-badge]][tests-workflow-url]\n[![PyPI][pypi-badge]][pypi-url]\n\n`fast-mda-traceroute` is an experimental multipath traceroute tool based on [caracal][caracal]\nand [diamond-miner][diamond-miner]. It aims to provide a faster alternative to [paris-traceroute][paris-traceroute]\nand [scamper][scamper] for running one-off measurements. It runs on Linux and macOS, on x86-64 and ARM64 systems.\n\n🚧 This tool is highly experimental, may not always work, and its interface is subject to change from one commit to\nanother.\n\n## Quickstart\n\n### Docker\n\n```bash\ndocker run ghcr.io/dioptra-io/fast-mda-traceroute --help\n```\n\nThe `latest` tag maps to the latest tagged commit and the `main` tag maps to the latest commit on the `main` branch.\n\n### Python\n\nYou can use pip, or [pipx][pipx] to install `fast-mda-traceroute` in a dedicated virtual environment:\n\n```bash\npipx install fast-mda-traceroute\nfast-mda-traceroute --help\n```\n\n## Usage\n\n```bash\n# Show help\nfast-mda-traceroute --help\n# Multipath traceroute towards example.org with default options\nfast-mda-traceroute example.org\n# Print paris-traceroute equivalent command\nfast-mda-traceroute --print-command=paris-traceroute example.org\n# Print scamper equivalent command\nfast-mda-traceroute --print-command=scamper example.org\n```\n\n`fast-mda-traceroute` outputs log messages to `stderr` and measurement results to `stdout`.\n\n## Development\n\n```bash\npoetry install\npoetry run fast-mda-traceroute --help\n```\n\n```bash\ndocker build -t fast-mda-traceroute .\ndocker run fast-mda-traceroute --help\n```\n\n[caracal]: https://github.com/dioptra-io/caracal\n\n[diamond-miner]: https://github.com/dioptra-io/diamond-miner\n\n[paris-traceroute]: https://paris-traceroute.net\n\n[pipx]: https://github.com/pypa/pipx/\n\n[scamper]: https://www.caida.org/catalog/software/scamper/\n\n[coverage-badge]: https://img.shields.io/codecov/c/github/dioptra-io/fast-mda-traceroute?logo=codecov&logoColor=white\n\n[coverage-url]: https://codecov.io/gh/dioptra-io/fast-mda-traceroute\n\n[docker-workflow-badge]: https://img.shields.io/github/workflow/status/dioptra-io/fast-mda-traceroute/Docker?logo=github&label=docker\n\n[docker-workflow-url]: https://github.com/dioptra-io/fast-mda-traceroute/actions/workflows/docker.yml\n\n[pypi-workflow-badge]: https://img.shields.io/github/workflow/status/dioptra-io/fast-mda-traceroute/PyPI?logo=github&label=pypi\n\n[pypi-workflow-url]: https://github.com/dioptra-io/fast-mda-traceroute/actions/workflows/pypi.yml\n\n[tests-workflow-badge]: https://img.shields.io/github/workflow/status/dioptra-io/fast-mda-traceroute/Tests?logo=github&label=tests\n\n[tests-workflow-url]: https://github.com/dioptra-io/fast-mda-traceroute/actions/workflows/tests.yml\n\n[pypi-badge]: https://img.shields.io/pypi/v/fast-mda-traceroute?logo=pypi&logoColor=white\n\n[pypi-url]: https://pypi.org/project/fast-mda-traceroute/\n',
    'author': 'Maxime Mouchet',
    'author_email': 'maxime.mouchet@lip6.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dioptra-io/fast-mda-traceroute',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
