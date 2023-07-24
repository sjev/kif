from kif.utils import create_example_config, get_config_path


def test_create_example_config():
    """create example config file in current dir"""

    fname = get_config_path()

    if fname.exists():
        fname.unlink()

    create_example_config(fname)
    assert fname.exists()
