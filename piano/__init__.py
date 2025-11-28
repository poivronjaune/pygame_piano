import tomllib
from pathlib import Path

try:
    from importlib.metadata import version, PackageNotFoundError
    __version__ = version("piano")
except PackageNotFoundError:
    __version__ = None
    raise RuntimeError("piano package is not installed properly. Check TOML file and use 'pip install -e .'")

def version():
    """Display piano version information."""
    print(f"piano version: {__version__}")

__all__ = ["__version__"]