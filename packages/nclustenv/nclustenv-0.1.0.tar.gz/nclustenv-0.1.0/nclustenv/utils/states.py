
import nclustgen
import numpy as np
from dgl.dataloading import GraphDataLoader
from torch.utils.data import SubsetRandomSampler

from .helper import loader, real_to_ind, clusters_from_bool
import torch as th

from dgl.data import DGLDataset


class State:

    """
    State class to store current environment state.
    """

    def __init__(self, generator='BiclusterGenerator', n=None, np_random=None, *args, **kwargs):

        """
        Parameters
        ----------

        generator: str or class, default BiclusterGenerator.
            The name of a generator from the nclustgen tool, or the class for a personalised generator (not advised).
        n: int, default None
            The number of clusters to find.
        np_random: pointer, default None
            Random State.

        Attributes
        ----------

        n: int
            The number of clusters to find.
        defined: object
            If the number of clusters to find is known
        cluster_coverage: list[float]
            An ordered list of with the percentage of coverage for every hidden cluster.

        """

        if np_random is None:
            np_random = np.random.RandomState()

        self._cls = loader(generator, nclustgen)
        self.n = n
        self.defined = n is not None

        self._generator = None
        self._ntypes = None
        self._np_random = np_random

        self.cluster_coverage = None

    @property
    def shape(self):

        """
        Returns the state's shape.

        Returns
        -------

            list
                Shape of current state.

        """
        return self._generator.X.shape

    @property
    def clusters(self):

        """
        Returns the current found clusters indexes (Current solution).

        Returns
        -------

            list
                Found clusters.

        """

        return clusters_from_bool(self.current, self._ntypes)

    @property
    def hclusters(self):
        """
        Returns hidden clusters index (Goal).

        Returns
        -------

            list
                Hidden clusters.

        """

        return self._generator.Y

    @property
    def hclusters_size(self):
        """
        Returns the size of the hidden clusters.

        Returns
        -------

            list[int]
                Ordered list hidden cluster sizes.

        """

        return [sum(map(len, cluster)) for cluster in self.hclusters]

    @property
    def max_hclusters_size(self):

        """
        Returns the current state clusters max possible size.

        Returns
        -------

            float
                Percentage of cluster coverage.

        """

        if not self.defined:

            return sum(self.hclusters_size)

        else:
            sizes = self.hclusters_size

            # Sliding window algorithm
            curr_sum = sum(sizes[:self.n])
            res = curr_sum
            for i in range(self.n, len(sizes)):
                curr_sum += sizes[i] - sizes[i - self.n]
                res = max(res, curr_sum)

            return res

    @property
    def coverage(self):

        """
        Returns the current state hidden cluster total coverage.

        Returns
        -------

            float
                Percentage of cluster coverage.

        """

        return self._generator.coverage

    @property
    def current(self):

        """
        Returns the current state graph.

        Returns
        -------

            dgl graph
                Current state graph.

        """

        return self._generator.graph

    @property
    def state(self):

        """
        Returns the state.

        Returns
        -------

            dict
                State

        """

        nclusters = len(self.clusters)

        # Check if add and remove actions are available
        add = np.full((len(self._ntypes), nclusters), True, dtype=bool)
        remove = np.full((len(self._ntypes), nclusters), True, dtype=bool)

        for i, ntype in enumerate(self._ntypes):
            for j in self.current.nodes[ntype].data:

                cluster = self.current.nodes[ntype].data[j]

                if cluster.all():
                    add[i][j] = False
                elif not cluster.any():
                    remove[i][j] = False

        add = add.any()
        remove = remove.any()

        if self.defined:
            mask = np.array([add, remove, False, False]).astype(int)

        else:
            merge = nclusters > 1
            mask = np.array([add, remove, merge, True]).astype(int)

        return {
            "action_mask": mask.astype(np.float32),
            "avail_actions": np.ones(len(mask), dtype=np.float32),
            "state": self.current
        }

    @property
    def as_dense(self):

        """
        Returns the current state as a dense array.

        Returns
        -------

            numpy array
                Current state as a dense array.

        """

        return self._generator.X

    def _set_cluster_coverage(self):
        """
        Returns a list of hidden clusters coverage.

        Returns
        -------

            list[float]
                Ordered list hidden cluster coverage.

        """

        max_size = self.max_hclusters_size
        sizes = self.hclusters_size

        return np.array([cluster/max_size for cluster in sizes])

    def _set_node(self, x, params):

        """
        Sets the cluster value for given node.

        Parameters
        ----------

        x: bool
            value to set
        params: list[float]
            List of parameters, [ntype, node, cluster], range: [0, 1]

        """

        if isinstance(x, bool):
            # parse param(ntype) into string
            ntype = self._ntypes[real_to_ind(self._ntypes, params[0])]
            # parse param(node) into index
            index = real_to_ind(self.current.nodes(ntype), params[1])
            # parse param(cluster) into index
            cluster = real_to_ind(self.current.nodes[ntype].data, params[2])
            # set value on node data
            self.current.nodes[ntype].data[cluster][index] = x

    def _reset_clusters_index(self):
        """
        Resets the index of the cluster in the graph.
        """

        keys = sorted(list(self.current.nodes[self._ntypes[0]].data.keys()))
        for i, key in enumerate(keys):
            self.current.ndata[i] = self.current.ndata.pop(key)

    def add(self, params):

        """
        Adds a given node to the cluster.

        Parameters
        ----------

        params: list[float]
            List of parameters, [ntype, node, cluster], range: [0, 1]

        """

        self._set_node(True, params[:3])

    def remove(self, params):

        """
        Removes a given node from the cluster.

        Parameters
        ----------

        params: list[float]
            List of parameters, [ntype, node, cluster], range: [0, 1]

        """

        self._set_node(False, params[:3])

    def merge(self, params):

        """
        Merges two clusters

        Parameters
        ----------

        params: list[float]
            List of parameters, [cluster1, cluster2], range: [0, 1]

        """

        params = params[:2]

        if not self.defined:

            # get index to set
            index = len(self.clusters)

            # parse params(clusters) into index
            cluster1, cluster2 = [real_to_ind(self.clusters, param) for param in params]

            # Set new cluster
            if cluster1 != cluster2:
                for ntype in self._ntypes:
                    self.current.nodes[ntype].data[index] = th.bitwise_or(
                        self.current.nodes[ntype].data[cluster1], self.current.nodes[ntype].data[cluster2]
                    )

                # Delete previous clusters
                self.current.ndata.pop(cluster1)
                self.current.ndata.pop(cluster2)

                # reset index
                self._reset_clusters_index()

    def split(self, params):

        """
        Splits two clusters

        Parameters
        ----------

        params: list[float]
            List of parameters, [cluster], range: [0, 1]

        """

        params = params[:1]

        if not self.defined:

            # get indexes to set
            index1 = len(self.clusters)
            index2 = index1 + 1

            # parse param(cluster) into index
            cluster = real_to_ind(self.clusters, params[0])

            for ntype in self._ntypes:

                # select partition point
                index = self._np_random.randint(
                    low=0, high=len(self.current.nodes[ntype].data[cluster]), dtype=np.int32
                )

                # create new clusters
                self.current.nodes[ntype].data[index1] = th.cat((
                    self.current.nodes[ntype].data[cluster][:index],
                    th.zeros(len(self.current.nodes[ntype].data[cluster][index:]), dtype=th.bool)),
                    0
                )

                self.current.nodes[ntype].data[index2] = th.cat((
                    th.zeros(len(self.current.nodes[ntype].data[cluster][:index]), dtype=th.bool),
                    self.current.nodes[ntype].data[cluster][index:]),
                    0
                )

            # delete previous cluster
            self.current.ndata.pop(cluster)

            # reset index
            self._reset_clusters_index()

    def _reset(self):

        # update ntype
        self._ntypes = [ntypes for ntypes in self.current.ntypes]
        self._ntypes.insert(0, self._ntypes.pop())

        # update cluster coverage
        self.cluster_coverage = self._set_cluster_coverage()

    def reset(self, shape, nclusters, settings=None, clust_init='zeros', **kwargs):

        """
        Resets the state (generates new state)

        Parameters
        ----------

        shape: list[int]
            Shape of new state.
        nclusters: int
            Number of hidden clusters.
        settings: dict
            Dataset settings (nclustgen).
        not_init: bool, default False
            If True clusters are not initialized.

            Note
            ----
                Use with care, this parameter might break the environment.

        Returns
        -------

            observation (object)
                The initial observation.

        """
        if settings is None:
            settings = {}

        # generate
        self._generator = self._cls(**settings)
        self._generator.generate(*shape, nclusters=nclusters)

        if kwargs.get('not_init'):
            self._generator.to_graph(framework='dgl', device='gpu', nclusters=0, clust_init=clust_init)
        elif self.defined:
            self._generator.to_graph(framework='dgl', device='gpu', nclusters=self.n, clust_init=clust_init)
        else:
            self._generator.to_graph(framework='dgl', device='gpu', clust_init=clust_init)

        self._reset()

        return self.state


class OfflineState(State):

    """
    Offline state class to store current environment state in offline environments.
    """

    def __init__(
            self,
            dataset,
            train_test_split=0.8,
            n=None,
            np_random=None,
            *args, **kwargs):
        """
        Parameters
        ----------

        dataset: class
             DGL dataset class.

        train_test_split: float, default 0.8
            The percentage for train/test split

        n: int, default None
            The number of clusters to find.

        np_random: pointer, default None
            Random object. If undefined np.random will be used

        Attributes
        ----------

        n: int
            The number of clusters to find.
        defined: object
            If the number of clusters to find is known
        cluster_coverage: list[float]
            An ordered list of with the percentage of coverage for every hidden cluster.

        """

        if not isinstance(dataset, DGLDataset):
            raise AttributeError('Dataset must inherit from DGLDataset class')

        if 0 > train_test_split or train_test_split > 1 :
            raise AttributeError('train_test_split must be between 0 and 1')

        super(OfflineState, self).__init__(
            n=n,
            np_random=np_random
        )

        num_examples = len(dataset)
        num_train = int(num_examples * train_test_split)

        train_sampler = SubsetRandomSampler(th.arange(num_train))
        test_sampler = SubsetRandomSampler(th.arange(num_train, num_examples))

        self._train_dataloader = GraphDataLoader(
            dataset, sampler=train_sampler, batch_size=1, drop_last=False)
        self._test_dataloader = GraphDataLoader(
            dataset, sampler=test_sampler, batch_size=1, drop_last=False)

        self._test_iter = 0
        self.graph = None
        self.label = None

    @property
    def shape(self):

        """
        Returns the state's shape.

        Returns
        -------

            list
                Shape of current state.

        """
        return tuple([list(self.current.nodes(axis).shape)[0] for axis in self._ntypes])

    @property
    def current(self):

        """
        Returns the current state graph.

        Returns
        -------

            dgl graph
                Current state graph.

        """

        return self.graph

    @property
    def hclusters(self):

        """
        Returns hidden clusters index (Goal).

        Returns
        -------

            list
                Hidden clusters.

        """

        return self.label

    def _init_clusts(self):

        """
        Initializes clusters on current graph
        """

        if self.defined:
            nclusters = self.n
        else:
            nclusters = 1

        for n, axis in enumerate(self._ntypes):
            for i in range(nclusters):
                self.graph.nodes[axis].data[i] = th.zeros(len(self.graph.nodes(axis)), dtype=th.bool)

    def reset(self, train=True, **kwargs):

        """
        Resets the state (generates new state)

        Parameters
        ----------

        train: bool
            If the algorithm is training.

        Returns
        -------

            observation (object)
                The initial observation.

        """

        if train:
            self.graph, self.label = next(self._train_dataloader.__iter__())
            self._reset()
            self._init_clusts()

            return self.state

        else:
            self.graph, self.label = next(self._test_dataloader.__iter__())
            self._reset()
            self._init_clusts()
            self._test_iter += 1

            return self.state, self._test_iter >= len(self._test_dataloader)








