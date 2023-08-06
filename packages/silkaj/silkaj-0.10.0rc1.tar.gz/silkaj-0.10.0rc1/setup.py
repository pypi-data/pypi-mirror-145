# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['silkaj']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.0,<9.0.0',
 'duniterpy==1.1.0',
 'pendulum>=2.1.2,<3.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'texttable>=1.6.3,<2.0.0']

entry_points = \
{'console_scripts': ['silkaj = silkaj.cli:cli']}

setup_kwargs = {
    'name': 'silkaj',
    'version': '0.10.0rc1',
    'description': 'Powerfull, lightweight, and multi-platform command line client written with Python for Duniter’s currencies: Ğ1 and Ğ1-Test.',
    'long_description': '<img src="https://git.duniter.org/clients/python/silkaj/raw/dev/logo/silkaj_logo.svg" width="250" />\n\n# Silkaj\n[![Version](https://img.shields.io/pypi/v/silkaj.svg)](https://pypi.python.org/pypi/silkaj)\n[![License](https://img.shields.io/pypi/l/silkaj.svg)](https://pypi.python.org/pypi/silkaj)\n[![Python versions](https://img.shields.io/pypi/pyversions/silkaj.svg)](https://pypi.python.org/pypi/silkaj)\n[![Code format](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![Coverage report](https://git.duniter.org/clients/python/silkaj/badges/dev/coverage.svg)](https://clients.duniter.io/python/silkaj/index.html)\n[![Website](https://img.shields.io/website/https/silkaj.duniter.org.svg)](https://silkaj.duniter.org)\n[![Dev pipeline status](https://git.duniter.org/clients/python/silkaj/badges/dev/pipeline.svg)](https://git.duniter.org/clients/python/silkaj/)\n\nPowerfull, lightweight, and multi-platform command line client written with Python for Ğ1 and Ğ1-Test currencies\n- [Website](https://silkaj.duniter.org)\n\n## Install\n### Distribution\nInstall with your favorite package manager. See below the [packaging status paragraph](#packaging-status).\n\n### Pip\nIf you want a more recent version [install with Pip](doc/install_pip.md):\n\n```bash\npip3 install silkaj --user\n```\n\n### Docker images\nThere is two kind of images. One build with `pip` for user purposes, and one using Poetry for developer purposes.\n- [Docker images](doc/docker.md)\n\n### For contributing purposes\n- [Install the Poetry development environment](doc/install_poetry.md)\n- Check out the [contributing guidelines](CONTRIBUTING.md)\n\n## Usage\n- Get help usage with `-h` or `--help` options, then run:\n```bash\nsilkaj <sub-command>\n```\n\n- Will automatically request and post data on `duniter.org 443` main Ğ1 node.\n\n- Specify a custom node with `-p` option:\n```bash\nsilkaj -ep <hostname>:<port> <sub-command>\n```\n\n## Features\n### Currency information & blockchain exploration\n- Check the present currency information stand\n- Display current proof of work difficulty level to generate the next block\n- Explore the blockchain block by block\n\n### Money management\n- Transaction emission\n  - Multi-recipients transaction support\n- Consult wallets balances\n- Consult wallet history\n\n### Web-of-Trust management\n- Look up for public keys and identities\n- Check sent and received certifications and consult the membership status of any given identity in the Web of Trust\n- Certification emission\n- Membership emission\n\n### Authentication\n- Authentication methods: Scrypt, file, and (E)WIF\n\n### Others\n- Display Ğ1 monetary license\n- Public key checksum\n\n## Wrappers\n- [Install as a drop-down for GNOME\xa0Shell with Argos](doc/argos.md)\n- [How-to: automate transactions and multi-output](doc/how-to_automate_transactions_and_multi-output.md)\n- [Transaction generator written in Shell](https://gitlab.com/jytou/tgen)\n- [Ğ1Cotis](https://git.duniter.org/matograine/g1-cotis)\n- [G1pourboire](https://git.duniter.org/matograine/g1pourboire)\n- [Ğ1SMS](https://git.duniter.org/clients/G1SMS/)\n- [Ğmixer](https://git.duniter.org/tuxmain/gmixer-py/)\n\n### Dependencies\nSilkaj is based on following Python modules:\n- [Click](https://click.palletsprojects.com/): Composable command line interface toolkit\n- [DuniterPy](https://git.duniter.org/clients/python/duniterpy/): Most complete client oriented Python library for Duniter/Ğ1 ecosystem\n- [Pendulum](https://pendulum.eustace.io/): Datetimes made easy\n- [texttable](https://github.com/foutaise/texttable/): Creation of simple ASCII tables\n- [tabulate](https://github.com/astanin/python-tabulate): Pretty-print tabular data\n\n### Names\nI wanted to call that program:\n- bamiyan\n- margouillat\n- lsociety\n- cashmere\n\nI finally called it `Silkaj` as `Silk` in esperanto.\n\n### Website\n- [Silkaj website sources](https://git.duniter.org/websites/silkaj_website/)\n\n## Packaging status\n[![Packaging status](https://repology.org/badge/vertical-allrepos/silkaj.svg)](https://repology.org/project/silkaj/versions)\n',
    'author': 'Moul',
    'author_email': 'moul@moul.re',
    'maintainer': 'Moul',
    'maintainer_email': 'moul@moul.re',
    'url': 'https://silkaj.duniter.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
