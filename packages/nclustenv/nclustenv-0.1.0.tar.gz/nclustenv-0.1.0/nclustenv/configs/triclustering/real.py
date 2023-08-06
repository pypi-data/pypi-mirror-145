
from nclustenv.configs.biclustering import real
from nclustenv.configs.triclustering import _modules
from nclustenv.utils.helper import inherit_config


base = inherit_config(real.base, _modules.tric_base, settings=_modules.tric_base_settings)
