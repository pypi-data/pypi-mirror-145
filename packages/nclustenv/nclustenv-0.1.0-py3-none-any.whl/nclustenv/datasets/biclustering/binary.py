
from nclustenv.utils.datasets import SyntheticDataset
from nclustenv.utils.helper import inherit_config
from nclustenv.configs.biclustering import binary
from nclustenv.datasets import SAVE_DIR


_synthetic_base = {
            'name': 'bic_binary_base',
            'length': 100,
            'seed': 7,
            'save_dir': SAVE_DIR,
            'generator': 'BiclusterGenerator'
        }

base = SyntheticDataset(**inherit_config(binary.base, _synthetic_base, drop='max_steps'))
