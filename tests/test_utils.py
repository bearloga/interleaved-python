from interleaved.utils import *
import numpy as np

def test_split():
    x = [1, 2, 3, 4, 5, 6]
    y = ['a', 'a', 'a', 'b', 'b', 'c']
    z = split(x, y)
    assert z == { 'a': [1, 2, 3], 'b': [4, 5], 'c': [6] }

def test_rescale():
    assert rescale(0, [-0.5, 0.5], [-1, 1]) == 0, "0 on [-0.5, 0.5] should be 0 on [-1, 1] scale"
    assert rescale(-0.5, [-0.5, 0.5], [-1, 1]) == -1, "-0.5 on [-0.5, 0.5] should be -1 on [-1, 1] scale"
    assert rescale(0.5, [-0.5, 0.5], [-1, 1]) == 1, "0.5 on [-0.5, 0.5] should be 1 on [-1, 1] scale"
    assert rescale(-0.25, [-0.5, 0.5], [-1, 1]) == -0.5, "-0.25 on [-0.5, 0.5] should be -0.5 on [-1, 1] scale"
    assert rescale(0.25, [-0.5, 0.5], [-1, 1]) == 0.5, "0.25 on [-0.5, 0.5] should be 0.5 on [-1, 1] scale"
    input = np.array([-0.125, 0.125])
    output = np.array([-0.25, 0.25])
    assert (rescale(input, [-0.5, 0.5], [-1, 1]) == output).all(), "NumPy ndarray should be rescaled correctly and remain a NumPy ndarray"

def test_outcome_determination():
    assert determine_outcome(['A']) == 'A', "Single click on A should yield A as winner"
    assert determine_outcome(['B']) == 'B', "Single click on B should yield B as winner"
    assert determine_outcome(['A', 'B']) == 'Draw', "Single clicks on A and B should yield a tie"
    assert determine_outcome(['A', 'B', 'A']) == 'A', "More clicks on A than B should yield A as winner"

def test_preference_calculation():
    assert preference(['A']) == 0.5, "Since A outcome should yield preference statistic of 0.5"
    assert preference(['B']) == -0.5, "Since B outcome should yield preference statistic of -0.5"
    assert preference(['A', 'B']) == 0, "One outcome for each should yield preference statistic of 0"
    assert preference(['A', 'B', 'Draw']) == 0, "Equal outcomes should yield preference statistic of 0"
    assert preference(['A', 'B', 'Draw', 'A', 'A', 'A']) == 0.25, "2x preference for A should yield statistic of 0.25"
    assert preference(['A', 'B', 'Draw', 'B', 'B', 'B']) == -0.25, "2x preference for B should yield statistic of 0.25"
