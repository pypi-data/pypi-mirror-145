# py\_pushover\_simple

[![PyPI version](https://badge.fury.io/py/py-pushover-simple.svg)](https://pypi.org/project/py-pushover-simple/)

This is a very simple python pushover wrapper for sending quick messages from command line scripts.

## Installation

1. Obtain the code:

    Download from PyPi *(recommended)*:

    ```shell
    python3 -m pip install py-pushover-simple
    ```

    or, clone the repository:

    ```shell
    git clone https://github.com/prplecake/py_pushover_simple
    ```

2. Add it to your script:

    ```python
    from py_pushover_simple import pushover

    def send_message(message):
        p = pushover.Pushover()
        p.user = 'user key'
        p.token = 'app token'

        p.sendMessage(message)
    ```

For a working demo, see [ippush.py] from the [ip_push] project.

## Usage

`py_pushover_simple` can be used on the command line:

For a full list of arguments:

```shell
$ python -m py_pushover_simple.pushover -h
usage: pushover.py [-h] [-u <string>] [-t <string>]

optional arguments:
  -h, --help   show this help message and exit
  -u <string>  pushover user token
  -t <string>  pushover app token
```

[ippush.py]:https://github.com/prplecake/ip_push/blob/master/ippush.py
[ip_push]:https://github.com/prplecake/ip_push/

## Resources

Additional documentation may be found [in the wiki][wiki].

[wiki]:https://github.com/prplecake/py_pushover_simple/wiki

This project is licensed under the terms of the MIT license.
