# wificitylogin

[![PyPI Status][pypi-workflow-badge]][pypi-workflow-url]
[![PyPI][pypi-badge]][pypi-url]

Automated login to the CIUP's (*Cité Internationale Universitaire de Paris*) Ethernet and Wi-Fi networks.

## Installation

```bash
pip install wificitylogin
```

## Usage

In your home directory, create a file name `.wificity` that contains your credentials:
```ini
[default]
username = ...
password = ...
```

For more security, you can restrict access to this file to your user only:
```bash
chmod 0600 ~/.wificity
```

Then, to log in to the network, run:
```bash
wificitylogin
```

[coverage-badge]: https://img.shields.io/codecov/c/github/maxmouchet/wificitylogin?logo=codecov&logoColor=white

[coverage-url]: https://codecov.io/gh/maxmouchet/wificitylogin

[pypi-workflow-badge]: https://img.shields.io/github/workflow/status/maxmouchet/wificitylogin/PyPI?logo=github&label=pypi

[pypi-workflow-url]: https://github.com/maxmouchet/wificitylogin/actions/workflows/pypi.yml

[tests-workflow-badge]: https://img.shields.io/github/workflow/status/maxmouchet/wificitylogin/Tests?logo=github&label=tests

[tests-workflow-url]: https://github.com/maxmouchet/wificitylogin/actions/workflows/tests.yml

[pypi-badge]: https://img.shields.io/pypi/v/wificitylogin?logo=pypi&logoColor=white

[pypi-url]: https://pypi.org/project/wificitylogin/
