

class Action:
    """"
    Action class to store the action for the environment.
    """

    def __init__(self, index, params, labels=None):
        """"

        Parameters
        ----------

        index: int
            The index of the selected action.

            ======== ===========
              Default Actions
            --------------------
            index    action
            ======== ===========
            0        add
            1        remove
            2        merge
            3        split
            ======== ===========

        params: list[list[floats]]
            The parameters of the actions.

            **Range**: [0, 1]

        """
        if labels is None:
            labels = ['add', 'remove', 'merge', 'split']

        self.index = index

        self._parameters = params
        self._labels = labels

    @property
    def action(self):

        """
        Returns the action selected.

        Returns
        -------

            str
                The selected action.

        """

        return self._labels[self.index]

    @property
    def parameters(self):
        """
        Returns the parameters related to the action selected.

        Returns
        -------

            list[float]
                The parameters related to this action.

        """

        return [float(max(min(param, 1.0), 0.0)) for param in self._parameters[self.index]]
