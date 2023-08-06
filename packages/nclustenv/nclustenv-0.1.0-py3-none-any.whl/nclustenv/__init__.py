
__author__      = "Pedro Cotovio"
__license__     = 'GNU GPLv3'

from nclustenv.version import VERSION as __version__

import os
import sys
import warnings

from gym import error

from gym.core import Env, GoalEnv, Wrapper, ObservationWrapper, ActionWrapper, RewardWrapper
from gym.envs import make, spec, register

from . import environments, datasets, configs, utils

