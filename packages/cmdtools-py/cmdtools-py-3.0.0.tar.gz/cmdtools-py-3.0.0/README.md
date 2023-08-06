<div id="headline" align="center">
  <h1>cmdtools</h1>
  <p>A module for parsing and processing commands.</p>
  <a href="https://github.com/HugeBrain16/cmdtools/actions/workflows/python-package.yml">
    <img src="https://github.com/HugeBrain16/cmdtools/actions/workflows/python-package.yml/badge.svg" alt="tests"></img>
  </a>
  <a href="https://pypi.org/project/cmdtools-py">
    <img src="https://img.shields.io/pypi/dw/cmdtools-py" alt="downloads"></img>
    <img src="https://badge.fury.io/py/cmdtools-py.svg" alt="PyPI version"></img>
    <img src="https://img.shields.io/pypi/pyversions/cmdtools-py" alt="Python version"></img>
  </a>
  <a href="https://codecov.io/gh/HugeBrain16/cmdtools">
    <img src="https://codecov.io/gh/HugeBrain16/cmdtools/branch/main/graph/badge.svg?token=mynvRn223H"/>
  </a>
  <a href='https://cmdtools-py.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/cmdtools-py/badge/?version=latest' alt='Documentation Status' />
  </a>
</div>

## Installation

```
pip install --upgrade cmdtools-py
```
install latest commit from GitHub  
```
pip install git+https://github.com/HugeBrain16/cmdtools.git
```

### Basic example

```py
import asyncio
import cmdtools

@cmdtools.callback.add_option("message")
def send(ctx):
    print(ctx.options.message)

@send.error
def error_send(ctx):
  if isinstance(ctx.error, cmdtools.NotEnoughArgumentError):
    if ctx.error.option == "message":
      print("Message is required!")

cmd = cmdtools.Cmd('/send hello')
asyncio.run(cmdtools.execute(cmd, send))
```

## Links

PyPI project: https://pypi.org/project/cmdtools-py  
Source code: https://github.com/HugeBrain16/cmdtools  
Issues tracker: https://github.com/HugeBrain16/cmdtools/issues  
Documentation: https://cmdtools-py.readthedocs.io/en/latest
