
from .base import BaseEnv
from nclustenv.utils.states import State, OfflineState
from nclustenv.utils.helper import tensor_to_string, index_to_tensor


class TriclusterEnv(BaseEnv):

    """
    This class provides an implementation of a three-dimensional gym environment with hidden triclusters.
    """

    def __init__(
            self,
            shape=None,
            n=None,
            clusters=None,
            dataset_settings=None,
            seed=None,
            metric='match_score',
            action='Action',
            max_steps=200,
            error_margin=0.05,
            penalty=0.001,
            init_state=True,
            *args, **kwargs
    ):

        if shape is None:
            shape = [[100, 100, 2], [200, 200, 5]]

        # Enforce shape size

        if len(shape[0]) != 3:
            raise AttributeError('Shape does not produce a tridimensional dataset')

        # Enforce ctx > 1
        if shape[0][-1] < 2:
            shape[0][-1] = 2
        elif shape[1][-1] < 2:
            shape[1][-1] = 2

        super(TriclusterEnv, self).__init__(
            shape=shape,
            n=n,
            clusters=clusters,
            dataset_settings=dataset_settings,
            seed=seed,
            metric=metric,
            action=action,
            max_steps=max_steps,
            error_margin=error_margin,
            penalty=penalty,
            *args, **kwargs
        )

        if init_state:
            self.state = State(generator='TriclusterGenerator', n=n, np_random=self.np_random)
            self.reset()

    def _render(self, index):
        print(tensor_to_string(index_to_tensor(self.state.as_dense, index), index))


class OfflineTriclusterEnv(TriclusterEnv):
    """
    This class provides an implementation of an offline two-dimensional gym environment with hidden biclusters.
    """

    def __init__(
            self,
            dataset,
            n=None,
            seed=None,
            metric='match_score',
            action='Action',
            max_steps=200,
            error_margin=0.05,
            penalty=0.001,
            train_test_split=0.8,
            *args, **kwargs
    ):
        """
        Parameters
        ----------

        dataset: SyntheticDataset
            DGLdataset to train on.
        n: int, default None
            Number of clusters to find, use None to train the undefined clusters tasks.
        seed: int, default None
            Seed to initialize random object.
        metric: str or class, default 'match_score_1_n'.
            The name of a metric implemented in `utils.metrics`, or a pointer for a personalised metric.

            ================ ===========
            Implemented metrics
            ----------------------------
            name             task
            ================ ===========
            match_score      Any
            ================ ===========

        action: str or class, default 'Action'.
            The name of a action class implemented in `utils.actions`, or a pointer for a personalised action class.
        max_steps: int, default 200
            Maximum number of actions an agent can perform in a given environment.
        error_margin: float, default 0.05
            Margin of error for agent.
        penalty: float, default 0.001
            Penalty on reward per timestep (discount factor).

        Attributes
        ----------

        dataset_settings: dict
            Dataset settings to be passed to generator.
        max_steps: int
            Maximum number of actions an agent can perform in a given environment.
        target: float
            Target margin for agent.
        penalty: float
            Penalty on reward per timestep (discount factor).
        action_space: gym space
            Space from where the agent samples actions.
        observation_space: gym space
            Space from where the environment samples observations.
        np_random: numpy random object
            Random object.
        state: state object
            State object.

        """

        super(OfflineTriclusterEnv, self).__init__(
            shape=dataset.shape,
            n=n,
            clusters=dataset.clusters,
            dataset_settings=dataset.settings,
            seed=seed,
            metric=metric,
            action=action,
            max_steps=max_steps,
            error_margin=error_margin,
            penalty=penalty,
            init_state=False,
            *args, **kwargs
        )

        self.state = OfflineState(dataset=dataset, train_test_split=train_test_split, n=n, np_random=self.np_random)
        self.reset()

    def reset(self, train=True):
        """
        Resets the environment to an initial state and returns an initial observation.
        Note that this function should not reset the environment's random
        number generator(s); random variables in the environment's state should
        be sampled independently between multiple calls to `reset()`. In other
        words, each call of `reset()` should yield an environment suitable for
        a new episode, independent of previous episodes.

        Returns
        -------
            observation (object)
                The initial observation.
        """

        # reset loggers
        self._current_step = 0
        self._steps_beyond_done = 0
        self._last_distances = [1.0, 1.0, 1.0]
        self._done = False

        return self.state.reset(train=train)
