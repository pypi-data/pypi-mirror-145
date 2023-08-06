
from nclustenv.datasets import SAVE_DIR
from nclustenv.configs.triclustering import binary
from nclustenv.utils.datasets import SyntheticDataset
from nclustenv.utils.helper import inherit_config

_synthetic_base = {
            'name': 'tric_binary_base',
            'length': 100,
            'seed': 7,
            'save_dir': SAVE_DIR,
            'generator': 'TriclusterGenerator'
        }

base = SyntheticDataset(**inherit_config(binary.base, _synthetic_base, drop='max_steps'))
