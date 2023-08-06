from nclustenv.configs.biclustering import binary
from nclustenv.utils.helper import inherit_config

_base = {
    'dataset_settings': {
        'dstype': dict(value='Numeric'),
        'realval': dict(value=True),
        'minval': dict(value=0),
        'maxval': dict(value=20),
        'patterns': dict(value=[['CONSTANT', 'CONSTANT']]),
        'bktype': dict(value='UNIFORM'),
        'clusterdistribution': dict(value=[['UNIFORM', 8, 12], ['UNIFORM', 4, 6]]),
        'contiguity': dict(value=None),
        'plaidcoherency': dict(value='NO_OVERLAPPING')
    }
}

base = inherit_config(binary.base, _base)


