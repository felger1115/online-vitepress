import os
import pathlib
from ruamel.yaml import YAML

config_dir = pathlib.Path(__file__).parent.absolute()

# load yaml
_file = config_dir / 'config.yaml'
_yaml = YAML(typ='safe')
file = _yaml.load(_file)


# load order: environment variable > config.yaml > default
_REQUIRED = object()
def get(path, default_value=_REQUIRED):
    # find in environment variables
    upath = path.upper().replace('.', '_')
    if upath in os.environ:
        return os.environ[upath]
    
    # find in yaml
    keys = path.lower().split('.')
    rv, miss = file, False
    for key in keys:
        if key not in rv:
            miss = True
            break
        rv = rv[key]
    if not miss:
        return rv

    # required
    if default_value is _REQUIRED:
        raise ValueError(f'{path} must be provided by either {_file}#{path.lower()} or environment variable {upath}.')
    return default_value


# set environment
env = get('env', 'dev').lower()
prod = (env == 'prod')
rev = (env == 'review')
dev = not prod and not rev
debug = not prod