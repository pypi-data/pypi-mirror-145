import sys

if sys.version_info[:2] >= (3, 8):  # pragma: nocover
    from importlib.metadata import version as importlib_metadata_version
else:  # pragma: nocover
    # Python 3.7 doesn't have this.
    from importlib_metadata import version as importlib_metadata_version


__version__ = importlib_metadata_version(__package__)
