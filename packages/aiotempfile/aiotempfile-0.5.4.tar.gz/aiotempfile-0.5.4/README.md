# aiotempfile

[![pypi version](https://img.shields.io/pypi/v/aiotempfile.svg)](https://pypi.org/project/aiotempfile)
[![build status](https://github.com/crashvb/aiotempfile/actions/workflows/main.yml/badge.svg)](https://github.com/crashvb/aiotempfile/actions)
[![coverage status](https://coveralls.io/repos/github/crashvb/aiotempfile/badge.svg)](https://coveralls.io/github/crashvb/aiotempfile)
[![python versions](https://img.shields.io/pypi/pyversions/aiotempfile.svg)](https://pypi.org/project/aiotempfile)
[![linting](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![license](https://img.shields.io/github/license/crashvb/aiotempfile.svg)](https://github.com/crashvb/aiotempfile/blob/master/LICENSE.md)

## Overview

Provides asynchronous temporary files.

## Installation
### From [pypi.org](https://pypi.org/project/aiotempfile/)

```
$ pip install aiotempfile
```

### From source code

```bash
$ git clone https://github.com/crashvb/aiotempfile
$ cd aiotempfile
$ virtualenv env
$ source env/bin/activate
$ python -m pip install --editable .[dev]
```

## Usage

This implementation is a derivation of [aiofiles](https://pypi.org/project/aiofile/) and functions the same way.

```python
import aiotempfile
async with aiotempfile.open() as file:
    file.write(b"data")
```

If the context manager is not used, files will need be explicitly closed; otherwise, they will only be removed during the interepreter teardown.

```python
import aiotempfile
file = await aiotempfile.open()
file.write(b"data")
file.close()
```

### Environment Variables

| Variable | Default Value | Description |
| ---------| ------------- | ----------- |
| AIOTEMPFILE_DEBUG | | Adds additional debug logging.

## Development

[Source Control](https://github.com/crashvb/aiotempfile)
