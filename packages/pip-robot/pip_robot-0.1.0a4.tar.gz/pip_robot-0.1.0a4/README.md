# pip-robot
[![pytest](https://github.com/ffreemt/pip-robot/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/pip-robot/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/pip_robot.svg)](https://badge.fury.io/py/pip_robot)

Install missing packages, automatically with best-effort

## Install it

```shell
pip install pip-robot

pip install git+https://github.com/ffreemt/pip-robot
# poetry add git+https://github.com/ffreemt/pip-robot
# git clone https://github.com/ffreemt/pip-robot && cd pip-robot
```

## Use it
```python
pip-robot python foo.py  # check agains one file

pip-robot "python -m bar"  # check against bar/__main__.py
```
