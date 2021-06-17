# interleaved

Library for analyzing interleaved search A/B tests to determine preference between competing [ranking functions](https://en.wikipedia.org/wiki/Ranking_(information_retrieval))

## Installing

```
pip install --upgrade git+https://github.com/bearloga/interleaved-python.git@main
```

## Usage

```python
from interleaved import load_example_data

data = load_example_data(preference='a') # alternatively: 'none' or 'b'

data.head()
```

```
                  timestamp   search_id  event  position ranking_function
0 2018-08-01 00:01:31+00:00  p2tvgm3clu   serp       NaN              NaN
1 2018-08-01 00:04:09+00:00  p2tvgm3clu  click      14.0                A
2 2018-08-01 00:04:29+00:00  p2tvgm3clu  click       4.0                A
3 2018-08-01 00:06:10+00:00  p2tvgm3clu  click       1.0                A
4 2018-08-01 00:06:42+00:00  p2tvgm3clu  click       7.0                B
```

```python
from interleaved import Experiment

ex = Experiment(
    queries = data[data['event'] == 'click']['search_id'].to_numpy(),
    clicks = data[data['event'] == 'click']['ranking_function'].to_numpy()
)
ex.bootstrap(seed=42)

print(ex.summary(ranker_labels=['New Algorithm', 'Old Algorithm'], rescale=True))
```

```
 In this interleaved search experiment, 906 searches were used to determine whether the
results from ranker 'New Algorithm' or 'Old Algorithm' were preferred by users (based on
their clicks to the results from those rankers interleaved into a single search result
set).

 The preference statistic, as defined by Chapelle et al. (2012), was estimated to be 74.3%
with a 95% (bootstrapped) confidence interval of (70.0%, 77.9%) on [-100%, 100%] scale
with -100% indicating total preference for 'Old Algorithm', 100% indicating total
preference for 'New Algorithm', and 0% indicating complete lack of preference between the
two -- indicating that the users had preference for ranker 'New Algorithm'.
```

Quite a strong preference for that new algorithm!

**Additional methods:**
- `.distribution(rescale=False)` returns the bootstrapped distribution of preference statistic (useful if visualizing)
- `.preference_statistic(rescale=False)` returns the estimated preference statistic
- `.conf_int(conf_level=0.95, rescale=False)` returns the confidence interval based on the bootstrapped distribution

**Note**: `rescale=True` rescales the preference statistic from [-0.5, 0.5] scale to a [-1, 1] scale,
which may help with interpretability of the results.

## References

- Chapelle, O., Joachims, T., Radlinski, F., & Yue, Y. (2012). Large-scale validation and analysis of interleaved search evaluation. *ACM Transactions on Information Systems*, **30**(1), 1-41. [doi:10.1145/2094072.2094078](https://doi.org/10.1145/2094072.2094078)
- Radlinski, F. and Craswell, N. (2013). [Optimized interleaving for online retrieval evaluation](https://www.microsoft.com/en-us/research/publication/optimized-interleaving-for-online-retrieval-evaluation/). *ACM International Conference on Web Search and Data Mining (WSDM)*. [doi:10.1145/2433396.2433429](https://doi.org/10.1145/2433396.2433429)
