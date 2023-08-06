
from pathlib import Path as _path
SAVE_DIR = _path.joinpath(_path(__file__).parent.absolute(), 'bin')

from . import biclustering, triclustering
