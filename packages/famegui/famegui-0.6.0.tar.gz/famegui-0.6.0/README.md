[![PyPI version](https://badge.fury.io/py/famegui.svg)](https://badge.fury.io/py/famegui)
[![PyPI license](https://img.shields.io/pypi/l/famegui.svg)](https://badge.fury.io/py/famegui)
[![pipeline status](https://gitlab.com/fame-framework/FAME-Gui/badges/master/pipeline.svg)](https://gitlab.com/fame-framework/FAME-Gui/commits/master)
[![coverage report](https://gitlab.com/fame-framework/FAME-Gui/badges/master/coverage.svg)](https://gitlab.com/fame-framework/FAME-Gui/-/commits/master) 

# FAME-GUI

Recommended tools version:
- Python 3.8
- PySide2 for Qt 5.15

```bash
pip3 install -r requirements.txt
```

## Install dev tools on Ubuntu 20.04

```bash
sudo apt install python3-pyside2.qtwidgets pyqt5-dev-tools qttools5-dev-tools qtcreator
```

## Running the app locally (from source)

```bash
python3 -m famegui
```

## Packaging the app (to deploy on PyPI)

> Make sure to add in your `~/.pypirc` the credentials required to publish a package on https://pypi.org/project/famegui/

```bash
pip3 install --user -U setuptools twine wheel

# create package (source distribution)
python3 setup.py sdist

# upload to PyPI
twine upload dist/*

# install the published package locally
pip3 install -U famegui
```
