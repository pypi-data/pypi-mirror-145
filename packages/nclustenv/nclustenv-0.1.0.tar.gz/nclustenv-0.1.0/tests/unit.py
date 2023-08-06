#!usr/bin/env python

'''
Tests to ensure environment components functionality is satisfied.
'''
import shutil
import traceback
import unittest
import pathlib as pl

import nclustenv
import nclustgen
import numpy as np
import os

import torch as th
import dgl

from nclustenv.utils.helper import loader, parse_ds_settings, isListEmpty
from nclustenv.utils.states import State, OfflineState
from nclustenv.utils.actions import Action
from nclustenv.environments.classic_lr import BiclusterEnv, TriclusterEnv
from nclustenv.utils.spaces import DGLHeteroGraphSpace
from nclustenv.utils.datasets import SyntheticDataset
from gym.spaces import Box

from nclustenv.version import TESTING_CONFIGS, TESTING_CONFIGS_DATASETS


class TestCaseBase(unittest.TestCase):

    @staticmethod
    def assertIsFile(path):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))

    @staticmethod
    def assertIsNotFile(path):
        if pl.Path(path).resolve().is_file():
            raise AssertionError("File exists: %s" % str(path))

    @staticmethod
    def _build_dataset(**kwargs):
        return SyntheticDataset(**kwargs)


class ActionTest(TestCaseBase):

    def setUp(self):

        envs = [BiclusterEnv(), TriclusterEnv()]
        self.scenarios = [env.action_space.sample() for env in envs for _ in range(100)]

        self.labels = ['add', 'remove', 'merge', 'split']

    def test_scenes(self):

        for scene in self.scenarios:

            action = Action(*scene)

            # Check if tupple is encoded into action object
            self.assertEqual(action.index, scene[0])
            self.assertTrue((action.parameters == scene[1][scene[0]]).all())

            # Check labels
            self.assertEqual(action.action, self.labels[scene[0]])

    def test_cropping(self):

        scene = tuple([0, [[2, -0.1, 1, 0, 0.5], [], [], []]])
        expected = [1, 0, 1, 0, 0.5]

        self.assertEqual(Action(*scene).parameters, expected)


class SpaceTest(TestCaseBase):
    def setUp(self):

        self.space = DGLHeteroGraphSpace(
            shape=[[100, 10], [200, 50]],
            n=5,
            clusters=[2, 5],
            settings={
                'fixed': {
                    'maxval': 5.0,
                    'silence': True,
                    'in_memory': True,
                    'seed': 5
                },
                'discrete': {'realval': [False, True]},
                'continuous': {'minval': [-1.0, 0.0]},
            }
        )

        self.state = State(n=5)
        self.state.reset(
            shape=[150, 30],
            nclusters=3,
            settings={
                'maxval': 5.0,
                'realval': True,
                'minval': 1.3,
                'silence': True,
                'in_memory': True,
                'seed': 5
            }
        )

    def test_contains(self):
        self.assertTrue(self.space.contains(self.state.current))

    def test_sample(self):

        for _ in range(50):
            self.assertTrue(self.space.contains(self.state.reset(*self.space.sample())['state']))


class StateTest(TestCaseBase):

    def setUp(self):

        self.states = [
           State(),
           State(n=4),
           State(generator='TriclusterGenerator', np_random=np.random.RandomState(4)),
           State(generator='TriclusterGenerator', n=5)
        ]

        for state in self.states:

            if 'Bicluster' in str(state._cls):
                shape = [100, 10]

            else:
                shape = [100, 10, 5]

            state.reset(
                shape=shape,
                nclusters=5,
                settings={'seed': 7, 'silence': True, 'in_memory': True}
            )

    def test_init(self):

        for state in self.states:

            # Check random is initialized
            self.assertTrue(state._np_random, type(np.random.RandomState()))

            # Check generator is initialized
            self.assertTrue(
                isinstance(state._cls, type(loader('TriclusterGenerator', nclustgen))) or
                isinstance(state._cls, type(loader('BiclusterGenerator', nclustgen)))
            )

    def test_reset(self):

        for state in self.states:

            # Check settings

            self.assertEqual(state._generator.seed, 7)

            # Check graph
            self.assertTrue(isinstance(state._generator.graph, dgl.DGLHeteroGraph))

            # Check cluster init
            if state.defined:
                self.assertEqual(len(state._generator.graph.nodes['row'].data.keys()), state.n)

            else:
                self.assertEqual(len(state._generator.graph.nodes['row'].data.keys()), 1)

            # check ntypes
            self.assertTrue(state._ntypes in [['row', 'col'], ['row', 'col', 'ctx']])

            # check cluster_coverage init
            self.assertTrue(isinstance(state.cluster_coverage, np.ndarray))

    def test_shape(self):

        for state in self.states:

            if state._generator._n == 2:
                self.assertEqual(state.shape, (100, 10))

            else:
                self.assertEqual(state.shape, (5, 100, 10))

    def test_clusters(self):

        for state in self.states:

            if 'Bicluster' in str(state._cls):
                shape = [100, 10]

            else:
                shape = [100, 10, 5]

            state.reset(
                shape=shape,
                nclusters=5,
                settings={'seed': 7, 'silence': True, 'in_memory': True}
            )

            if state.defined:

                self.assertEqual(
                    state.clusters,
                    [[[] for _ in range(state._generator._n)] for _ in range(state.n)]
                )

    def test_hclusters(self):

        for state in self.states:
            self.assertEqual(state.hclusters, state._generator.Y)

    def test_coverage(self):

        for state in self.states:

            self.assertEqual(state.coverage, state._generator.coverage)

    def test_current(self):

        for state in self.states:
            self.assertEqual(state.current, state._generator.graph)

    def test_state(self):

        for state in self.states:

            if state.defined:
                mask = [1, 0, 0, 0]
            else:
                mask = [1, 0, 0, 1]

            self.assertEqual(state.state['state'], state.current)
            self.assertTrue((state.state['action_mask'] == mask).all())
            self.assertTrue((state.state['avail_actions'] == np.ones(len(mask))).all())

    def test_dense(self):

        for state in self.states:
            self.assertTrue((state.as_dense == state._generator.X).all())

    def test_set_cluster_coverage(self):

        for state in self.states:

            if state.defined:

                diff = len(state.hclusters) - state.n
                if diff < 1:
                    diff = False

                if diff:
                    self.assertTrue(sum(state._set_cluster_coverage()[diff:]) == 1)

                else:
                    self.assertTrue(sum(state._set_cluster_coverage()) == 1)

            else:
                self.assertTrue(sum(state._set_cluster_coverage()) == 1)

    def test_basic_actions(self):

        for state in self.states:

            # check add
            state.add([0.1, 0.3, 0.1])
            self.assertTrue(state.clusters[0][0][0] == int(0.3*max(state.shape)))

            # check remove
            state.remove([0.1, 0.3, 0.1])

            if state.defined:
                n = state.n
            else:
                n = 1

            self.assertEqual(
                state.clusters,
                [[[] for _ in state._ntypes] for _ in range(n)]
            )

    def test_complex_actions(self):

        for state in self.states:

            if not state.defined:
                state.add([0.1, 0.3, 0.1])
                state.add([0.6, 0.6, 0.1])
                state.add([0.1, 0.5, 0.1])

                original_len = len(state.clusters)
                original_cluster = state.clusters[0]

                # check split
                state.split([0.1])

                ## check cluster order
                self.assertEqual(
                    list(state.current.nodes[state._ntypes[0]].data.keys()),
                    sorted(list(state.current.nodes[state._ntypes[0]].data.keys()))
                )

                ## division
                self.assertEqual(
                    len(state.clusters),
                    original_len + 1
                )

                ## values
                self.assertEqual(
                    np.sum(np.sum(original_cluster)),
                    np.sum(np.sum([state.clusters[-1], state.clusters[-2]]))
                )

                # check merge
                e = 0.0001
                state.merge([
                    (len(state.clusters) - 1 + e) / len(state.clusters),
                    (len(state.clusters) - 2 + e) / len(state.clusters)
                ])

                self.assertEqual(len(state.clusters), original_len)
                self.assertEqual(state.clusters[-1], original_cluster)


class SyntheticDatasetTest(TestCaseBase):

    def setUp(self) -> None:
        self.scenarios = TESTING_CONFIGS_DATASETS
        self.datasets = []

    def tearDown(self) -> None:

        while any(self.datasets):
            ds = self.datasets.pop()
            folder_path = os.path.join(ds.save_path)

            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

    def test_make(self):

        for configs in self.scenarios:
            for config in configs:

                tb = None

                try:
                    ds = self._build_dataset(**config)
                    self.datasets.append(ds)
                    success = True

                    # Check correct build
                    self.assertEqual(ds.shape, config['shape'])
                    self.assertEqual(ds.clusters, config['clusters'])
                    if config.get('dataset_settings'):
                        self.assertEqual(ds.settings, parse_ds_settings(config['dataset_settings']))

                    # Check save
                    self.assertIsFile(os.path.join(ds.save_path, ds.name + '_dgl_graph.bin'))
                    self.assertIsFile(os.path.join(ds.save_path, ds.name + '_info.pkl'))

                except Exception as e:
                    tb = e.__traceback__
                    success = False

                self.assertTrue(success, ''.join(traceback.format_tb(tb)))

    def test_load(self):

        self.test_make()

        for configs in self.scenarios:
            for config in configs:

                ds = self._build_dataset(
                    name=config['name'],
                    save_dir=config['save_dir']
                )

                # Check correct load
                self.assertEqual(ds.shape, config['shape'])
                self.assertEqual(ds.clusters, config['clusters'])

                if config.get('dataset_settings'):
                    self.assertEqual(ds.settings, parse_ds_settings(config['dataset_settings']))


class OfflineStateTest(TestCaseBase):

    def setUp(self) -> None:

        self.scenarios = zip(TESTING_CONFIGS[2:], TESTING_CONFIGS_DATASETS)
        self.datasets = []
        self.states = []

    def tearDown(self) -> None:

        while any(self.datasets):
            ds = self.datasets.pop()
            folder_path = os.path.join(ds.save_path)

            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

        self.states = []

    def test_make(self):

        for configs, ds_configs in self.scenarios:
            for config, ds_config in zip(configs, ds_configs):

                tb = None

                try:
                    ds = self._build_dataset(**ds_config)
                    self.datasets.append(ds)

                    state = OfflineState(ds, **config)
                    self.states.append(state)
                    success = True

                    # Check build
                    state.reset()

                    self.assertTrue(
                        Box(low=np.array(ds.shape[0]), high=np.array(ds.shape[1])).contains(np.array(state.shape))
                    )
                    self.assertTrue(isListEmpty(state.clusters))
                    self.assertFalse(state.current is None)
                    self.assertFalse(state.label is None)

                except Exception as e:
                    tb = e.__traceback__
                    success = False

                self.assertTrue(success, ''.join(traceback.format_tb(tb)))

    def test_reset(self):

        self.test_make()

        self.assertTrue(any(self.states))

        for state in self.states:

            for _ in range(len(state._train_dataloader) * 2):
                s = state.reset()

                self.assertTrue(isListEmpty(state.clusters))
                self.assertFalse(state.current is None)
                self.assertFalse(state.label is None)
                self.assertEqual(state.current, s['state'])

            for i in range(len(state._test_dataloader) * 2):
                s, done = state.reset(train=False)

                self.assertTrue(isListEmpty(state.clusters))
                self.assertFalse(state.current is None)
                self.assertFalse(state.label is None)
                self.assertEqual(state.current, s['state'])

                if i+1 >= len(state._test_dataloader):
                    self.assertTrue(done)
                    break

                self.assertFalse(done)
















