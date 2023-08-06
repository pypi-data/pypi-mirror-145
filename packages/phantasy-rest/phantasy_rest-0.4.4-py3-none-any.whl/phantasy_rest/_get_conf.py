import os
import toml
import tempfile

_cdir = os.path.dirname(os.path.abspath(__file__))


def read_config(path=None):
    """Read the .toml configuration file if provided, otherwise use the
    one distributed with the package.
    """
    if path is None:
        path = os.path.join(_cdir, 'config.toml')
    app_conf = toml.load(path)
    return app_conf


def set_envs(toml_path):
    """Set environmental variables from loaded .toml configuration file to drive gunicorn.
    """
    c = read_config(os.path.abspath(os.path.expanduser(toml_path)))
    for sec in ('LATTICE', 'GUNICORN'):
        for k, v in c[sec].items():
            os.environ[f"PH_{k}"] = str(v)


default_app_conf = read_config()
