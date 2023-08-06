# Python 3 library and CLI for [SporeStack](https://sporestack.com) [.onion](http://spore64i5sofqlfz5gq2ju4msgzojjwifls7rok2cti624zyq3fcelad.onion)

## Requirements

* Python 3.7-3.10 (or maybe newer)

## Installation

* `pip install sporestack`
* Recommended: Create a virtual environment, first, and use it inside there.

## Running without installing

* Make sure `pipx` is installed.
* `pipx run sporestack`
* Make sure you're on the latest stable version comparing `sporestack version` with git tags in this repository, or releases on [PyPI](https://pypi.org/project/sporestack/).

## Usage

* `sporestack token create --dollars 20 --currency xmr  # Can use btc as well.`
* `sporestack token list`
* `sporestack token balance`
* `sporestack server launch SomeHostname --operating-system debian-11 --days 1  # Will use ~/.ssh/id_rsa.pub as your SSH key, by default`
(You may also want to consider passing `--region` to have a non-random region. This will use the "primary" token by default, which is the default when you run `sporestack token create`.)
* `sporestack server stop SomeHostname`
* `sporestack server start SomeHostname`
* `sporestack server list`
* `sporestack server remove SomeHostname # If expired`

## Notes

* If you want to communicate with SporeStack APIs using Tor, set this environment variable: `SPORESTACK_USE_TOR_ENDPOINT=1`

## Developing

* `pip install pipenv pre-commit`
* `pre-commit install`
* `pipenv install --deploy --dev`
* `pipenv run make test` (If you don't have `make`, use `almake`)
* `pre-commit run --all-files` (To format code, or wait for `git commit`)

## Licence

[Unlicense/Public domain](LICENSE.txt)
