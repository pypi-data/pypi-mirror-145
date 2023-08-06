
from .classic_lr import BiclusterEnv, OfflineBiclusterEnv, TriclusterEnv, OfflineTriclusterEnv

from gym.envs import register

# Online Environments
register(id='BiclusterEnv-v0',
         entry_point='nclustenv.environments.classic_lr.biclusterenv:BiclusterEnv'
         )

register(id='TriclusterEnv-v0',
         entry_point='nclustenv.environments.classic_lr.triclusterenv:TriclusterEnv'
         )

# Offline Enviroments
register(id='OfflineBiclusterEnv-v0',
         entry_point='nclustenv.environments.classic_lr.biclusterenv:OfflineBiclusterEnv'
         )

register(id='OfflineTriclusterEnv-v0',
         entry_point='nclustenv.environments.classic_lr.triclusterenv:OfflineTriclusterEnv'
         )
