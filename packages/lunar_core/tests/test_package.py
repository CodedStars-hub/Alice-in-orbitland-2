from importlib.metadata import version

import lunar_core


def test_installed_package_version() -> None:
    assert lunar_core.__version__ == version("lunar-core")
