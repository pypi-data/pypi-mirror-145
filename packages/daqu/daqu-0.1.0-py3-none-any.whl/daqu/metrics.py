from pydantic import BaseModel
import pandas as pd
from datetime import datetime
from typing import Optional, List


def zero_denominator(func):
    """
    Decorator that returns None when ZeroDivisionError occurs

    :param func:
    :return:
    """

    def check_denom(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ZeroDivisionError:
            return None

    return check_denom


@zero_denominator
def normalized_accuracy(value: float, truth: float, **kwargs):
    """
    :param value:
    :param truth:
    :param kwargs:
    :return:
    """
    return abs(truth - value) / abs(truth)


def difference_of_days(
        date_1: str, date_2: str,
        dt_format: str = "%Y-%m-%d"
):
    """
    Returns days between dates:  date_2 - date_1

    :param date_1:
    :param date_2:
    :return:
    """
    delta = datetime.strptime(date_2, dt_format) - datetime.strptime(date_1, dt_format)
    return delta.days


def observation_indices(release: pd.Series):
    """
    Return a list of the indices for which a value is listed
    :param release:
    :return: list
    """
    return release.index[release.notna()].tolist()


def restated(prior: float, cur: float, tol: float=0) -> bool:
    return abs(prior - cur) > tol


@zero_denominator
def percent_restated(prior: pd.Series, cur: pd.Series, rest_func=restated) -> float:
    """
    Return the percent of newly reported values that do not equal prior release's values
    :param prior:
    :param cur:
    :param rest_func:
    :return:
    """
    prior_obsvs = observation_indices(prior)
    cur_obsvs = observation_indices(cur)
    obsvs = [obsv for obsv in cur_obsvs if obsv in prior_obsvs]
    restated_num = sum([rest_func(prior, cur) for prior, cur in zip(prior[obsvs], cur.loc[obsvs])])
    return restated_num / len(obsvs)


def retroactive_change(prior: pd.Series, cur: pd.Series, phi: float = .5, **kwargs) -> bool:
    """
    Assess if a new release constitutes a retroactive change
    :param prior:
    :param cur:
    :param phi: minimum percent of values restated needed to consider a release a retroactive change
    :return: True if a retroactive change, o.w. False
    """
    perc = percent_restated(prior, cur, **kwargs)
    if perc >= phi:
        return True
    else:
        return False


class Metric(BaseModel):
    name: str
    data: Optional[pd.DataFrame]
    truth: Optional[pd.Series]
    expected_release: Optional[pd.Series]
    evaluated: Optional[pd.Series]

    def function(self, *args, **kwargs):
        return True

    class Config:
        arbitrary_types_allowed = True


class ObservationMetric(Metric):
    pass


class ReleaseMetric(Metric):

    def evaluate(self, release: pd.Series, truth: pd.Series):
        pass


class SeqReleaseMetric(Metric):

    def evaluate(self, data: pd.DataFrame, **kwargs):
        metrics = []

        for prior, cur in zip(data.columns[:-1], data.columns[1:]):
            metrics.append(self.function(prior=data[prior], cur=data[cur], **kwargs))

        self.evaluated = pd.Series(metrics, data.columns[1:])


class RetroactiveChange(SeqReleaseMetric):
    name = "Retroactive Change"

    def function(self, **kwargs):
        return retroactive_change(**kwargs)


class PercentRestated(SeqReleaseMetric):
    name = "Percent Restated"

    def function(self, **kwargs):
        return percent_restated(**kwargs)