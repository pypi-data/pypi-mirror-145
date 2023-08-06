
import gym
from dgl import DGLHeteroGraph
from .helper import retrive_skey
import numpy as np
import torch as th


class DGLHeteroGraphSpace(gym.spaces.Box):

    """
    Implementation of a DGLGraph space.
    """

    def __init__(
            self,
            shape,
            n=None,
            clusters=None,
            settings=None,
            np_random=None,
            clust_init='zeros',
            *args, **kwargs

    ):

        """
        Parameters
        ----------

        shape: list, default [[100, 100, 2], [200, 200, 5]]
            List of length 2 where the first element is the minimum shape the observation space and the second is the
            maximum.
        clusters: [int], default [1, 1]
            List of length 2 where the first element is the minimum number of cluster to be hidden in the environment
            and the second is the maximum.
        settings: dict, default {}
            Dataset settings to be passed to generator.

            **Format**: {parameter: {value: None, randomize: Bool}, type: {'Categorical', 'Continuous'}

            If randomize is True, value should contain a list with the values to sample from or the range.

            Examples
            --------
            >>> settings = {'bkype': {'value': ['NORMAL', 'UNIFORM'], 'randomize': True, 'type': 'Categorical'},
            >>> 'patterns': {'value': [['Order_Preserving', 'None'], ['None', 'Order_Preserving']], 'randomize': False,
            >>> 'type': 'Categorical'},
            >>> 'mean': {'value': [1.0, 14.0], 'randomize': True, 'type': 'Continuous'}
            >>> }

            Note
            ----
                Parameters `silence`, `in_memory` and `seed` should not be set, and will be overwritten.
        np_random: numpy random object
            Random object.
        """

        if np_random is None:
            np_random = np.random.RandomState()

        if clusters is None:
            clusters = [1, 1]

        if settings is None:
            settings = {
                'fixed': {},
                'discrete': {},
                'continuous': {},
            }

        self.n = n
        self.clusters = clusters
        self.settings = settings
        self._np_random = np_random
        self.clust_init = clust_init

        super(DGLHeteroGraphSpace, self).__init__(
            low=np.array(shape[0]),
            high=np.array(shape[1]),
            *args, **kwargs
        )

    def _sample(self, low, high, discrete=True) -> int:

        """
        Returns a random sample from a defined space.

        Returns
        -------

            int or float
                Space random sample.

        """

        try:
            if discrete:
                return self.np_random.randint(low=low, high=high)
            else:
                return self.np_random.uniform(low=low, high=high)
        except ValueError:
            return low

    def _node_labels(self, labels):

        """Returns node labels"""

        res = [ntypes for ntypes in labels]
        res.insert(0, res.pop())

        return res

    def sample(self):

        """
        Returns a sample of the space.

        Returns
        -------

            list
                Dataset shape.

            int
                Number of clusters.

            dict
                Dataset advanced settings.

        """

        # Sample basic settings
        shape = super(DGLHeteroGraphSpace, self).sample()
        nclusters = self._sample(*self.clusters)

        # Get Settings
        settings = {'seed': self.np_random.randint(low=1, high=10 ** 9, dtype=np.int32)}

        ## Fixed
        for key, value in self.settings['fixed'].items():
            settings[key] = value

        ## Discrete
        for key, value in self.settings['discrete'].items():
            settings[key] = value[self._sample(0, len(value))]

        ## Continuous
        for key, value in self.settings['continuous'].items():
            settings[key] = self._sample(low=value[0], high=value[1], discrete=False)

        return shape, nclusters, settings, self.clust_init

    def contains(self, x: DGLHeteroGraph) -> bool:

        # Enforce CPU
        if x.device.type != 'cpu':
            x = x.to('cpu')

        # Retrive shape
        shape = np.array([x.nodes(ntype).shape[0] for ntype in self._node_labels(x.ntypes)], dtype=self.dtype)

        # Check initialization
        if x.ndata['feat']:
            check = x.ndata['feat'][self._node_labels(x.ntypes)[0]].shape[1]

        else:
            check = len(x.nodes[self._node_labels(x.ntypes)[0]].data)

        if self.n:
            init = check == self.n
        else:
            init = check > 0

        # Verify settings
        if isinstance(x.edata['w'], dict):
            edata = x.edata['w'].copy()
            edata = th.cat([edata[edge] for edge in edata.keys()])

        else:
            edata = x.edata['w']

        if 'NUMERIC' in retrive_skey('dstype', self.settings, 'NUMERIC'):

            values = np.array(
                [minval <= edata.min().item() for minval in retrive_skey('minval', self.settings, -10.0)]
            ).any() \
                     and np.array(
                [maxval >= edata.max().item() for maxval in retrive_skey('maxval', self.settings, 10.0)]
            ).any()

            realval = np.array(
                [realval == edata.isreal().all().item() for realval in retrive_skey('realval', self.settings, True)]
            ).any()

            settings = realval and values

        else:
            symbols = retrive_skey('symbols', self.settings)

            if symbols is None:
                symbols = [[i for i in range(nsymbols)] for nsymbols in retrive_skey('nsymbols', self.settings, 10)]

            settings = np.array([edata.apply_(lambda y: y in s).bool().all().item() for s in symbols]).any()

        return (
            isinstance(x, DGLHeteroGraph)
            and super(DGLHeteroGraphSpace, self).contains(shape)
            and init
            and settings
        )



