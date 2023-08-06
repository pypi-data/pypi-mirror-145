import numpy as np


def IoU(x, y):

    """
    Returns the intersection over union for cluster `x`,  and cluster `y`.
    """

    intersection = sum([len(list(set(sx).intersection(sy))) for sx, sy in zip(x, y)])
    union = sum([(len(sx) + len(sy)) for sx, sy in zip(x, y)]) - intersection
    return float(intersection) / union


def match_score(fclusts, hclusts):

    """
    For any given cluster in `fclusts` (found clusters), returns the Jacquard distance of every element of `hclusts`
    (hidden clusters).
    """
    return np.array([[1-IoU(x, y) for y in hclusts] for x in fclusts])
