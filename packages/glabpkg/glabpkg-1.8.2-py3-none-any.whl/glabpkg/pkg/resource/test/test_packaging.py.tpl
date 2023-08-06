import {{ base.pkg_full_name }}


def test_package_exists():
    assert {{ base.pkg_full_name }}.__version__
