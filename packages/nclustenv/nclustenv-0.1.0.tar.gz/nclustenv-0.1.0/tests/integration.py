#!usr/bin/env python

'''
Tests to ensure environments load and basic functionality
is satisfied.
'''
import os
import shutil
import unittest
import nclustenv
from nclustenv.utils.datasets import SyntheticDataset
from nclustenv.version import ENV_LIST, TESTING_CONFIGS, TESTING_CONFIGS_DATASETS
import traceback


class TestCaseBase(unittest.TestCase):

    @staticmethod
    def _build_env(env_name, **kwargs):
        env = nclustenv.make(env_name, **kwargs)
        return env

    @staticmethod
    def _build_dataset(**kwargs):
        return SyntheticDataset(**kwargs)


class TestOnlineEnvs(TestCaseBase):

    def setUp(self):
        self.scenarios = zip(ENV_LIST[:2], TESTING_CONFIGS[:2])

    def test_make(self):
        # Ensures that environments are instantiated

        for env_name, configs in self.scenarios:
            for config in configs:

                tb = None

                try:
                    _ = self._build_env(env_name, **config)
                    success = True
                except Exception as e:
                    tb = e.__traceback__
                    success = False

                self.assertTrue(success, ''.join(traceback.format_tb(tb)))

    def test_episode(self):
        # Run 5 episodes and check observation space

        for env_name, configs in self.scenarios:
            for config in configs:

                EPISODES = 5
                env = self._build_env(env_name, **config)
                for ep in range(EPISODES):
                    state = env.reset()
                    while True:
                        self.assertTrue(env.observation_space.contains(state),
                                        f"State out of range of observation space: {state}")

                        action = env.action_space.sample()
                        state, reward, done, info = env.step(action)
                        if done:
                            break

                    self.assertTrue(done)


class TestOfflineEnvs(TestCaseBase):

    def setUp(self):
        self.scenarios = zip(ENV_LIST[2:], TESTING_CONFIGS[2:], TESTING_CONFIGS_DATASETS)
        self.datasets = []

    def tearDown(self) -> None:

        while any(self.datasets):
            ds = self.datasets.pop()
            folder_path = os.path.join(ds.save_path)

            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

    def test_make(self):
        # Ensures that environments are instantiated

        for env_name, configs, ds_configs in self.scenarios:
            for config, ds_config in zip(configs, ds_configs):

                tb = None

                try:
                    ds = self._build_dataset(**ds_config)
                    self.datasets.append(ds)

                    _ = self._build_env(env_name, dataset=ds, **config)
                    success = True

                except Exception as e:
                    tb = e.__traceback__
                    success = False

                self.assertTrue(success, ''.join(traceback.format_tb(tb)))

    def test_episode(self):
        # Run 5 episodes and check observation space

        for env_name, configs, ds_configs in self.scenarios:
            for config, ds_config in zip(configs, ds_configs):

                EPISODES = 5

                ds = self._build_dataset(**ds_config)
                self.datasets.append(ds)

                env = self._build_env(env_name, dataset=ds, **config)

                for ep in range(EPISODES):
                    state = env.reset()
                    while True:
                        self.assertTrue(env.observation_space.contains(state),
                                        f"State out of range of observation space: {state}")

                        action = env.action_space.sample()
                        state, reward, done, info = env.step(action)
                        if done:
                            break

                    self.assertTrue(done)
