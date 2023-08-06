# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['network_hash_gen',
 'network_hash_gen.cisco_ios',
 'network_hash_gen.juniper_junos']

package_data = \
{'': ['*']}

install_requires = \
['passlib>=1.7.4,<2.0.0', 'scrypt>=0.8.20,<0.9.0']

setup_kwargs = {
    'name': 'network-hash-gen',
    'version': '0.1.0',
    'description': 'A library to generate hashes for network devices.',
    'long_description': '# Network Hash Gen\n\nGenerating hashes for network devices like routers and switches - with the\noption to specify seeds or salts.\n\n# Currently supported hashes:\n\n- Cisco IOS/IOS-XE\n  - Type 5\n  - Type 9\n- Juniper JunOS\n  - Type 1\n  - Type 6\n\nIf you are missing a hash function, please open an issue.\n\n# Example\n\nThis example generates a hash with a random salt and a hash with a given seed.\nThe first function returns a different hash most of the times while the\nsecond one always returns the same hash value.\n\n``` python3\n>>> from network_hash_gen.cisco_ios import Type9\n>>> Type9.hash("foobar")\n\'$9$FteIXKc69u9886$JFenYTrYz7kgex.60fbd8kzIg3Y/fE8lhsrtZeiif8k\'\n>>> Type9.hash_seeded("foobar", "$hostname-$username")\n\'$9$XpsDCh72ruxTQc$Cm80vIgCAQPhWrLJczX53Z7qVg0AxKui6t8.QbWfBsU\'\n```\n\n# Installation\n\nThis package can be installed from PyPi via pip or whatever you prefer for\ndependency management.\n\n```\npip install network-hash-gen\n```\n\n# Documentation\n\nThe documentation build against the current master branch can be found here:\nhttps://991jo.github.io/network_hash_gen\n\nTo build the documentation for a specific version run\n\n```\npdoc3 --html --template-dir=templates network_hash_gen\n```\n\nThis will generate documentation in a folder called `html`.\n\n# Development\n\n## Setup\n\nThis project uses [poetry](https://python-poetry.org/).\n\nClone this repository, then run\n```\npoetry install\n```\nThis will create a venv and install the dev dependencies.\n\n## Running the tests\n\nThe tests are in the `tests` folder and are executed with\n\n```\npython3 -m unittest\n```\n\nThe unittests are also run via the pre-commit hooks.\n\nTo get test coverage reports [coverage](https://coverage.readthedocs.io/en/latest/)\nis used. Run \n\n```\ncoverage run -m unittest\n```\n\nto run the tests and `coverage report` for a CLI report of `coverage html` to\ngenerate a HTML version of the coverage report.\n\n## Code Formatting\n\nThe code in this repository is formated with [black](https://github.com/psf/black).\nThe default settings are used.\nPlease format the code with black before commiting.\nThis can be done with\n\n```\nblack network_hash_gen/\n```\n\nThe code formatting is also checked (but not executed) in the commit hooks.\n\n## Pre-Commit Hooks\n\nThere are pre-commit hooks that check the code formating and run the unittests.\nTo activate them, link the script in `scripts/pre-commit.sh` into your git hooks\ndirectory:\n\n```\ncd .git/hooks/\nln -s ../../scripts/pre-commit\n```\n',
    'author': 'Johannes Erwerle',
    'author_email': 'jo+network_hash_gen@swagspace.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/991jo/network_hash_gen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
