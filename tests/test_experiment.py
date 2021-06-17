from interleaved import Experiment
from interleaved.sessions import load_sessions
import pytest

# Re-used across first couple of tests:
data = load_sessions('none')
ex = Experiment(
    data[data['event'] == 'click']['search_id'].to_numpy(),
    data[data['event'] == 'click']['ranking_function'].to_numpy()
)

def test_type_error():
    with pytest.raises(TypeError):
        Experiment(
            data[data['event'] == 'click']['search_id'],
            data[data['event'] == 'click']['ranking_function']
        )

def test_bootstrapping():
    ex.bootstrap(n=1000, seed=42)
    dist = ex.distribution()
    assert dist.size == 1000, "Bootstrapped distribution should contain 1000 samples"

def test_no_preference():
    ci = ex.conf_int(conf_level=0.95)
    assert ex.preference_statistic() < 0.05, "Statistic should be close to 0 (less than 0.05)"
    assert (ci['lower'] < 0) & (ci['upper'] > 0), "95% CI should contain 0"

def test_a_preference():
    data = load_sessions('a')
    ex = Experiment(
        data[data['event'] == 'click']['search_id'].to_numpy(),
        data[data['event'] == 'click']['ranking_function'].to_numpy()
    )
    ex.bootstrap(n=100, seed=42)
    ci = ex.conf_int(conf_level=0.95)
    assert ex.preference_statistic() > 0, "Statistic should be positive (preference for A)"
    assert ci['lower'] > 0, "95% CI should be to the right of 0"

def test_b_preference():
    data = load_sessions('b')
    ex = Experiment(
        data[data['event'] == 'click']['search_id'].to_numpy(),
        data[data['event'] == 'click']['ranking_function'].to_numpy()
    )
    ex.bootstrap(n=100, seed=42)
    ci = ex.conf_int(conf_level=0.95)
    assert ex.preference_statistic() < 0, "Statistic should be negative (preference for B)"
    assert ci['upper'] < 0, "95% CI should be to the left of 0"
