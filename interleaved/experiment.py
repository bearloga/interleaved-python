import numpy as np
from interleaved.utils import split
from interleaved.utils import determine_outcome
from interleaved.utils import preference
from interleaved.utils import rescale as scale
from collections import Counter
from sklearn.utils import resample
from textwrap import wrap
from textwrap import dedent

class Experiment:
    """Class for analyzing preference in an interleaved search result experiment

    Methods
    -------
    bootstrap(n=1000, seed=None)
        Bootstrap the distribution of the preference statistic
    preference_statistic(rescale=False)
        Get the estimated preference statistic
    distribution(rescale=False)
        Bootstrapped distribution of the preference statistic
    conf_int(conf_level=0.95, rescale=False)
        Confidence interval for the preference statistic
    summary(conf_level=0.95, rescale=False, ranker_labels=['A', 'B'])
        Summary of the results, useful for including in a report

    Notes
    -----
    Calculation of the preference statistic is done according to the
    formula in [1]_. For more information about resampling (used for the
    p-value and confidence interval) refer to [2]_.

    References
    ----------
    [1] Chapelle, O., Joachims, T., Radlinski, F., & Yue, Y. (2012).
        Large-scale validation and analysis of interleaved search evaluation.
        ACM Transactions on Information Systems, 30(1), 1-41.
    [2] Bruce, P., Bruce, A., & Gedeck, P. (2020).
        Practical Statistics for Data Scientists (2nd Edition). O'Reilly Media.
    """

    def __init__(self, queries, clicks):
        """Initialize an Interleaved Experiment

        Parameters
        ----------
        clicks : array_like
            Array of 'A' and 'B', each representing a click on either A's or
            B's result within a set of search results
        queries : array_like
            IDs for grouping sets of clicks together under the same query

        """
        if not isinstance(clicks, np.ndarray):
            raise TypeError("Clicks must be a NumPy ndarray")
        if not isinstance(queries, np.ndarray):
            raise TypeError("Clicks must be a NumPy ndarray")

        searches = split(x = clicks, f = queries)
        outcomes = [determine_outcome(v) for k, v in searches.items()]
        self._outcomes = outcomes
        self._preference_statistic = preference(outcomes)

    def bootstrap(self, n=1000, seed=None):
        """Bootstraps distributions of preference statistics

        Parameters
        ----------
        n : int, default=1000
            Number of resamples to perform
        seed : int
            For reproducing specific results
        """
        rs = np.random.RandomState(seed)
        bootstrapped_preferences = []
        for _ in range(n):
            resampled_outcomes = resample(self._outcomes, random_state = rs)
            bootstrapped_preferences.append(preference(resampled_outcomes))

        self._bootstrapped_preferences = np.array(bootstrapped_preferences)

    def distribution(self, rescale=False):
        """Returns bootstrapped distribution of the preference statistic

        Parameters
        ----------
        rescale : bool, default False
            Whether to rescale the statistic from its original scale
            of [-0.5, 0.5] to a more easily interpretable [-1, 1].
        """
        return self._bootstrapped_preferences if not rescale else scale(self._bootstrapped_preferences, [-0.5, 0.5], [-1, 1])

    def preference_statistic(self, rescale=False):
        """Get the estimated preference statistic

        When there is no preference, the resulting statistic is close to 0 and
        the confidence interval includes 0.

        When users click on the interleaved results with a preference for 'A',
        the resulting preference statistic is *positive*. When users' preference
        is for 'B', the resulting statistic is *negative*.

        Parameters
        ----------
        rescale : bool, default False
            Whether to rescale the statistic from its original scale
            of [-0.5, 0.5] to a more easily interpretable [-1, 1].

        Returns
        -------
        float
        """
        return self._preference_statistic if not rescale else scale(self._preference_statistic, [-0.5, 0.5], [-1, 1])

    def conf_int(self, conf_level=0.95, rescale=False):
        """Get the confidence interval of the preference statistic

        Parameters
        ----------
        conf_level : float, default=0.95
            Level to generate confidence intervals for (e.g. 95%)
        rescale: bool, default False
            Whether to rescale the statistic from its original scale
            of [-0.5, 0.5] to a more easily interpretable [-1, 1].

        Returns
        -------
        dict
            lower : float
                Lower bound of the confidence interval
            upper : float
                Upper bound of the confidence interval
        """
        if not hasattr(self, '_bootstrapped_preferences'):
            print("Running bootstrap() with default settings")
            self.bootstrap()

        alpha = 1-conf_level
        bootstrapped_prefs = self._bootstrapped_preferences if not rescale else scale(self._bootstrapped_preferences, [-0.5, 0.5], [-1, 1])
        quantiles = np.round(np.quantile(bootstrapped_prefs, [alpha/2, 1-(alpha/2)]), decimals = 4)
        return dict(zip(['lower', 'upper'], quantiles))

    def summary(self, conf_level=0.95, rescale=False, ranker_labels=['A', 'B']):
        # Data for the report:
        n_searches = len(self._outcomes)
        estimate = np.round(self.preference_statistic(rescale=rescale), decimals = 4)
        ci = self.conf_int(conf_level, rescale)
        # Conclusions based on results:
        if ci['lower'] > 0:
            winner = ranker_labels[0]
        elif ci['upper'] < 0:
            winner = ranker_labels[1]
        else:
            winner = 'Draw'

        result = "no preference for either ranker" if winner == "Draw" else f"preference for ranker '{winner}'"

        # Rescale (if requested) for better interpretability:
        if rescale:
            estimate = f"{(estimate):.{1}%}"
            ci['lower'] = f"{(ci['lower']):.{1}%}"
            ci['upper'] = f"{(ci['upper']):.{1}%}"
            [scale_min, scale_mid, scale_max] = ["-100%", "0%", "100%"]
        else:
            [scale_min, scale_mid, scale_max] = ["-0.5", "0", "0.5"]

        # Put it all together:
        line_width = 90
        intro = f"""
        In this interleaved search experiment, {n_searches} searches were used to
        determine whether the results from ranker '{ranker_labels[0]}' or '{ranker_labels[1]}'
        were preferred by users (based on their clicks to the results from those rankers
        interleaved into a single search result set).
        """
        intro = "\n".join(wrap(dedent(intro), width=line_width))
        results = f"""
        The preference statistic, as defined by Chapelle et al. (2012), was estimated
        to be {estimate} with a {(conf_level):.{0}%} (bootstrapped) confidence interval
        of ({ci['lower']}, {ci['upper']}) on [{scale_min}, {scale_max}] scale with
        {scale_min} indicating total preference for '{ranker_labels[1]}', {scale_max}
        indicating total preference for '{ranker_labels[0]}', and {scale_mid} indicating
        complete lack of preference between the two -- indicating that the users had {result}.
        """
        results = "\n".join(wrap(dedent(results), width=line_width))
        report = intro + "\n\n" + results
        return report
