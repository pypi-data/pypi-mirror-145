
from dgl.data import DGLDataset
import numpy as np

from nclustenv.utils.spaces import DGLHeteroGraphSpace
from nclustenv.utils.helper import parse_ds_settings
from nclustenv.utils.states import State

import os
from dgl import save_graphs, load_graphs
from dgl.data.utils import save_info, load_info


class SyntheticDataset(DGLDataset):

    """
    Implementation of a DGLDataset, that creates a synthetic dataset with a given number of examples.
    """

    def __init__(
            self,
            length=10,
            shape=None,
            clusters=None,
            dataset_settings=None,
            seed=None,
            generator='BiclusterGenerator',
            name='synthetic',
            save_dir=None,
            verbose=False,
            *args, **kwargs
    ):
        """
        Parameters
        ----------

        length: int, default 10
            Number of examples to be generated.
        shape: list, default None
            List of length 2 where the first element is the minimum shape the observation space and the second is the
            maximum.
        clusters: [int], default [1, 1]
            List of length 2 where the first element is the minimum number of cluster to be hidden in the environment
            and the second is the maximum.
        dataset_settings: dict, default {}
            Dataset settings to be passed to generator.

            **Format**: {parameter: {value: None, randomize: Bool}, type: {'Categorical', 'Continuous'}

            If randomize is True, value should contain a list with the values to sample from or the range.

            Examples
            --------
            >>> dataset_settings = {'bkype': {'value': ['NORMAL', 'UNIFORM'], 'randomize': True, 'type': 'categorical'},
            >>> 'patterns': {'value': [['Order_Preserving', 'None'], ['None', 'Order_Preserving']], 'randomize': False,
            >>> 'type': 'categorical'},
            >>> 'mean': {'value': [1.0, 14.0], 'randomize': True, 'type': 'continuous'}
            >>> }

            Note
            ----
                Parameters `silence`, `in_memory` and `seed` should not be set, and will be overwritten.
        seed: int, default None
            Seed to initialize random object.
        generator: str or class, default BiclusterGenerator.
            The name of a generator from the nclustgen tool, or the class for a personalised generator (not advised).
        name: str, default synthetic
            Name of the dataset.
        save_dir: str, default None
            Directory to save the processed dataset.
        verbose: bool, default False
            Whether to print out progress information.

        Attributes
        ----------

        graphs: list
            Dataset's Graphs.
        labels: list
            Dataset's Labels.

        """

        if dataset_settings is None:
            dataset_settings = {}

        if clusters is None:
            clusters = [1, 1]

        self.graphs = None
        self.labels = None

        self._n = length

        np_random = np.random.RandomState(seed)

        self._observation_space = {
                'shape': shape,
                'n': None,
                'clusters': clusters,
                'settings': parse_ds_settings(dataset_settings),
                'np_random': np_random,
                'dtype': np.int32
        }

        self._state = {
            'generator': generator,
            'n': None,
            'np_random': np_random
        }

        super().__init__(
            name=name,
            raw_dir=save_dir,
            verbose=verbose
        )

    def process(self):

        _observation_space = DGLHeteroGraphSpace(**self._observation_space)
        _state = State(**self._state)

        self.graphs = []
        self.labels = []

        for _ in range(self._n):
            _state.reset(*_observation_space.sample(), not_init=True)
            self.graphs.append(_state.current)
            self.labels.append(_state.hclusters)

    def save(self):
        # save graphs and labels
        graph_path = os.path.join(self.save_path, self.name + '_dgl_graph.bin')
        save_graphs(graph_path, self.graphs)
        # save other information in python dict
        info_path = os.path.join(self.save_path, self.name + '_info.pkl')
        save_info(info_path, {
            'labels': self.labels,
            'observation_space': self._observation_space,
            'state': self._state
        })

    def load(self):
        # load processed data from directory `self.save_path`
        graph_path = os.path.join(self.save_path, self.name + '_dgl_graph.bin')
        self.graphs, label_dict = load_graphs(graph_path)
        info_path = os.path.join(self.save_path, self.name + '_info.pkl')
        self.labels = load_info(info_path)['labels']
        self._observation_space = load_info(info_path)['observation_space']
        self._state = load_info(info_path)['state']
        self._n = len(self.graphs)

    def has_cache(self):
        # check whether there are processed data in `self.save_path`
        graph_path = os.path.join(self.save_path, self.name + '_dgl_graph.bin')
        info_path = os.path.join(self.save_path, self.name + '_info.pkl')
        return os.path.exists(graph_path) and os.path.exists(info_path)

    @property
    def shape(self):

        """
        Returns the dataset's shape bounds.

        Returns
        -------

            list
                Shape Bounds.
        """

        return self._observation_space['shape']

    @property
    def clusters(self):

        """
        Returns the dataset's cluster bounds.

        Returns
        -------

            list
                Cluster Bounds.
        """
        return self._observation_space['clusters']

    @property
    def settings(self):

        """
        Returns the dataset's settings.

        Returns
        -------

            dict
                Dataset's settings.
        """

        return self._observation_space['settings']

    def __getitem__(self, i):
        return self.graphs[i], self.labels[i]

    def __len__(self):
        return len(self.graphs)
