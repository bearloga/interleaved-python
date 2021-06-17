import numpy as np
from collections import defaultdict
from collections import Counter

def rescale(x, old, new):
    return new[0] + (x - old[0])*(new[1]-new[0])/(old[1]-old[0])

def split(x, f):
    """Split x by f

    Parameters
    ----------
    x : array_like
        Values to split; must be same size as f
    f : array_like
        Factor to split by; must be same size as x
    """
    z = list(zip(f, x))
    output = defaultdict(list)
    for k, v in z:
        output[k].append(v)

    return dict(output)

def determine_outcome(clicks):
    counts = Counter(clicks)
    n_a = counts['A'] if 'A' in counts else 0
    n_b = counts['B'] if 'B' in counts else 0

    if n_a > n_b:
        return 'A'
    elif n_a < n_b:
        return 'B'
    else:
        return 'Draw'

def preference(outcomes):
    """Calculate the preference statistic

    Parameters
    ----------
    outcomes : dict
    """
    counts = Counter(outcomes) # { 'A':#, 'B':#, 'Draw':# }
    wins_A = counts['A'] if 'A' in counts else 0
    wins_B = counts['B'] if 'B' in counts else 0
    ties = counts['Draw'] if 'Draw' in counts else 0
    return ((wins_A + (ties/2)) / (wins_A + wins_B + ties)) - 0.5
