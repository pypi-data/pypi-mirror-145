# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests']

package_data = \
{'': ['*']}

modules = \
['vault2vault']
install_requires = \
['ruamel.yaml>=0.17.16,<0.18.0']

extras_require = \
{'ansible': ['ansible-core>=2.11.5,<3.0.0']}

entry_points = \
{'console_scripts': ['vault2vault = vault2vault:main']}

setup_kwargs = {
    'name': 'vault2vault',
    'version': '0.1.0',
    'description': 'Recursively rekey ansible-vault encrypted files and in-line variables',
    'long_description': "# vault2vault\n\nLike\n[`ansible-vault rekey`](https://docs.ansible.com/ansible/latest/cli/ansible-vault.html#rekey)\nbut works recursively on encrypted files and in-line variables\n\n[![CI Status](https://github.com/enpaul/vault2vault/workflows/CI/badge.svg?event=push)](https://github.com/enpaul/vault2vault/actions)\n[![PyPI Version](https://img.shields.io/pypi/v/vault2vault)](https://pypi.org/project/vault2vault/)\n[![License](https://img.shields.io/pypi/l/vault2vault)](https://opensource.org/licenses/MIT)\n[![Python Supported Versions](https://img.shields.io/pypi/pyversions/vault2vault)](https://www.python.org)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n⚠️ **This project is alpha software and is under active development** ⚠️\n\n- [What is this?](#what-is-this)\n- [Installing](#installing)\n- [Using](#using)\n- [Developing](#developer-documentation)\n\n## What is this?\n\nIf you use [Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html)\nthen you may have encountered the problem of needing to role your vault password. Maybe\nyou found it written down on a sticky note, maybe a coworker who knows it left the\ncompany, maybe you accidentally typed it into Slack when you thought the focus was on your\nterminal. Whatever, these things happen.\n\nThe builtin tool Ansible provides,\n[`ansible-vault rekey`](https://docs.ansible.com/ansible/latest/cli/ansible-vault.html#rekey),\nworks suffers from two main drawbacks: first, it only works on vault encrypted files and\nnot on vault encrypted YAML data; and second, it only works on a single vault encrypted\nfile at a time. To rekey everything in a large project you'd need to write a script that\ngoes through every file and rekeys everything in every format it can find.\n\nThis is that script.\n\n## Installing\n\nIf you're using [Poetry](https://python-poetry.org/) or\n[Pipenv](https://pipenv.pypa.io/en/latest/) to manage your Ansible runtime environment,\nyou can just add `vault2vault` to that same environment:\n\n```\n# using poetry\npoetry add vault2vault --dev\n\n# using pipenv\npipenv install vault2vault\n```\n\nIf you're using Ansible from your system package manager, it's probably easier to just\ninstall `vault2vault` using [PipX](https://pypa.github.io/pipx/) and the `ansible` extra:\n\n```\npipx install vault2vault[ansible]\n```\n\n**Note: vault2vault requires an Ansible installation to function. If you are installing to a standalone virtual environment (like with PipX) then you must install it with the `ansible` extra to ensure a version of Ansible is available to the application.**\n\n## Using\n\nThese docs are pretty sparse, largely because this project is still under active design\nand redevelopment. Here are the command line options:\n\n```\n> vault2vault --help\nusage: vault2vault [-h] [--version] [--interactive] [-v] [-b] [-i VAULT_ID] [--ignore-undecryptable] [--old-pass-file OLD_PASS_FILE]\n                   [--new-pass-file NEW_PASS_FILE]\n                   [paths ...]\n\nRecursively rekey ansible-vault encrypted files and in-line variables\n\npositional arguments:\n  paths                 Paths to search for Ansible Vault encrypted content\n\noptions:\n  -h, --help            show this help message and exit\n  --version             Show program version and exit\n  --interactive         Step through files and variables interactively, prompting for confirmation before making each change\n  -v, --verbose         Increase verbosity; can be repeated\n  -b, --backup          Write a backup of every file to be modified, suffixed with '.bak'\n  -i VAULT_ID, --vault-id VAULT_ID\n                        Limit rekeying to encrypted secrets with the specified Vault ID\n  --ignore-undecryptable\n                        Ignore any file or variable that is not decryptable with the provided vault secret instead of raising an error\n  --old-pass-file OLD_PASS_FILE\n                        Path to a file with the old vault password to decrypt secrets with\n  --new-pass-file NEW_PASS_FILE\n                        Path to a file with the new vault password to rekey secrets with\n```\n\nPlease report any bugs or issues you encounter on\n[Github](https://github.com/enpaul/vault2vault/issues).\n\n## Developer Documentation\n\nAll project contributors and participants are expected to adhere to the\n[Contributor Covenant Code of Conduct, v2](CODE_OF_CONDUCT.md) ([external link](https://www.contributor-covenant.org/version/2/0/code_of_conduct/)).\n\nThe `devel` branch has the latest (and potentially unstable) changes. The stable releases\nare tracked on [Github](https://github.com/enpaul/vault2vault/releases),\n[PyPi](https://pypi.org/project/vault2vault/#history), and in the\n[Changelog](CHANGELOG.md).\n\n- To report a bug, request a feature, or ask for assistance, please\n  [open an issue on the Github repository](https://github.com/enpaul/vault2vault/issues/new).\n- To report a security concern or code of conduct violation, please contact the project\n  author directly at **\u200cme \\[at\u200c\\] enp dot\u200e \u200cone**.\n- To submit an update, please\n  [fork the repository](https://docs.github.com/en/enterprise/2.20/user/github/getting-started-with-github/fork-a-repo)\n  and [open a pull request](https://github.com/enpaul/vault2vault/compare).\n\nDeveloping this project requires [Python 3.7+](https://www.python.org/downloads/) and\n[Poetry 1.0](https://python-poetry.org/docs/#installation) or later. GNU Make can\noptionally be used to quickly setup a local development environment, but this is not\nrequired.\n\nTo setup a local development environment:\n\n```bash\n# Clone the repository...\n# ...over HTTPS\ngit clone https://github.com/enpaul/vault2vault.git\n# ...over SSH\ngit clone git@github.com:enpaul/vault2vault.git\n\ncd vault2vault/\n\n# Create and configure the local development environment...\nmake dev\n\n# Run tests and CI locally...\nmake test\n\n# See additional make targets\nmake help\n```\n",
    'author': 'Ethan Paul',
    'author_email': '24588726+enpaul@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/enpaul/vault2vault/',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
