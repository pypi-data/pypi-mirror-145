# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['wificitylogin']
install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0', 'requests>=2.27.0,<3.0.0']

entry_points = \
{'console_scripts': ['wificitylogin = wificitylogin:main']}

setup_kwargs = {
    'name': 'wificitylogin',
    'version': '1.0.1',
    'description': "Automated login to the CIUP's Ethernet and Wi-Fi networks.",
    'long_description': "# wificitylogin\n\n[![PyPI Status][pypi-workflow-badge]][pypi-workflow-url]\n[![PyPI][pypi-badge]][pypi-url]\n\nAutomated login to the CIUP's (*Cité Internationale Universitaire de Paris*) Ethernet and Wi-Fi networks.\n\n## Installation\n\n```bash\npip install wificitylogin\n```\n\n## Usage\n\nIn your home directory, create a file name `.wificity` that contains your credentials:\n```ini\n[default]\nusername = ...\npassword = ...\n```\n\nFor more security, you can restrict access to this file to your user only:\n```bash\nchmod 0600 ~/.wificity\n```\n\nThen, to log in to the network, run:\n```bash\nwificitylogin\n```\n\n[coverage-badge]: https://img.shields.io/codecov/c/github/maxmouchet/wificitylogin?logo=codecov&logoColor=white\n\n[coverage-url]: https://codecov.io/gh/maxmouchet/wificitylogin\n\n[pypi-workflow-badge]: https://img.shields.io/github/workflow/status/maxmouchet/wificitylogin/PyPI?logo=github&label=pypi\n\n[pypi-workflow-url]: https://github.com/maxmouchet/wificitylogin/actions/workflows/pypi.yml\n\n[tests-workflow-badge]: https://img.shields.io/github/workflow/status/maxmouchet/wificitylogin/Tests?logo=github&label=tests\n\n[tests-workflow-url]: https://github.com/maxmouchet/wificitylogin/actions/workflows/tests.yml\n\n[pypi-badge]: https://img.shields.io/pypi/v/wificitylogin?logo=pypi&logoColor=white\n\n[pypi-url]: https://pypi.org/project/wificitylogin/\n",
    'author': 'Maxime Mouchet',
    'author_email': 'max@maxmouchet.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maxmouchet/wificitylogin',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
