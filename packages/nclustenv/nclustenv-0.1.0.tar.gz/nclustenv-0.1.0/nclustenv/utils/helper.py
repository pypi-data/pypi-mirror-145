import collections.abc
import torch as th

def index_to_matrix(x, index):

    """Returns a sub-matrix of `x` given by the `index`."""

    return [[x[row][col] for col in index[1]] for row in index[0]]


def index_to_tensor(x, index):

    """Returns a sub-tensor of `x` given by the `index`."""

    return [index_to_matrix(x[ctx], index[:2]) for ctx in index[2]]


def matrix_to_string(matrix, index=None, title=''):

    """Returns a matrix as a printable string"""

    if index:
        temp = [[title] + ['y{}'.format(i) for i in index[1]]]
        for i, idx in enumerate(index[0]):

            idx = 'x{}'.format(idx)

            try:
                temp.append([idx] + matrix[i])
            except IndexError:
                temp.append(idx)

        matrix = temp

    return '\n'.join([''.join(['{:10}'.format(str(item)) for item in row]) for row in matrix])


def tensor_to_string(tensor, index=None):

    """Returns a tensor as a printable string"""

    title = ['' for _ in tensor]

    if index:
        title = ['z{}'.format(i) for i in index[2]]
        index = index[:2]

    return '\n\n'.join([matrix_to_string(ctx, index, title[i]) for i, ctx in enumerate(tensor)])


def loader(cls, module=None):

    """Loads a method from a pointer or a string"""

    return getattr(module, cls) if isinstance(cls, str) else cls


def real_to_ind(x, param):
    """Parses real values into list indexes"""

    return int(round(param * (len(x)-1), 0))


def clusters_from_bool(graph, ntypes):

    """Returns the clusters of a graph as a list of lists"""

    keys = [key for key in graph.nodes[ntypes[0]].data.keys()]

    return [[[i
              for i, val in enumerate(graph.nodes[ntype].data[j]) if val]
             for ntype in ntypes]
            for j in keys]


def parse_ds_settings(settings, enforced=None):

    """Parse dataset settings into actionable dict"""

    if enforced is None:
        enforced = {
            'silence': True,
            'in_memory': True,
            'seed': None
        }

    new_settings = {
        'fixed': {},
        'discrete': {},
        'continuous': {},
    }

    keys = list(settings.keys())

    if keys != list(new_settings.keys()):

        # Enforce fixed settings

        for key in list(enforced.keys()):
            if key in keys:
                keys.remove(key)

            new_settings['fixed'][key] = enforced[key]

        for key in keys:
            if settings[key].get('randomize', False):
                if settings[key]['type'].lower() == 'categorical':
                    new_settings['discrete'][key] = settings[key]['value']

                elif settings[key]['type'].lower() == 'continuous':
                    new_settings['continuous'][key] = settings[key]['value']

            else:
                new_settings['fixed'][key] = settings[key]['value']

        return new_settings
    return settings


def retrive_skey(key: str, settings: dict, default=None):

    """Retrives a key from parsed settings"""

    groups = ['fixed', 'discrete', 'continuous']

    for group in groups:
        val = settings[group].get(key)

        if val:
            if group == 'fixed':
                return [val]
            return val

    return [default]


def parse_bool_input(x, default=True):

    """Parses an Y/n input into bool"""

    if x:
        if x in ['Y', 'y']:
            return True
        elif x in ['N', 'n']:
            return False

    return bool(default)


def isListEmpty(x):

    """Returns if all nested lists are empty"""

    if isinstance(x, list):
        return all(map(isListEmpty, x))
    return False


def _inherit_dict(parent, child):

    res = parent.copy()
    res.update(child)

    return res


def inherit_config(parent, child, settings=None, drop=None):

    res = parent.copy()
    res.update(child)
    if drop:

        drop = list(drop)

        for key in drop:
            res.pop(key, None)

    if settings:

        res['dataset_settings'] = res['dataset_settings'].copy()
        res['dataset_settings'].update(settings)

    return res


def randint(size, dtype):
    return th.randint(low=0, high=2, size=[size], dtype=dtype)






