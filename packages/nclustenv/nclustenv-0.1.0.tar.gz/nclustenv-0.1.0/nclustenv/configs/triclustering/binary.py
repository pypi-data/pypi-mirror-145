
from nclustenv.configs.biclustering import binary
from nclustenv.configs.triclustering import _modules
from nclustenv.utils.helper import inherit_config

base = inherit_config(binary.base, _modules.tric_base, settings=_modules.tric_base_settings)
