import pandas

from . import _cnsts
from ._query import Query
from ._utils import rest_client


class KairosDB:
    def __init__(self, uri: str, check_health: bool = True):
        if uri.endswith("/"):
            uri = uri.removesuffix("/")
        self.uri = uri
        if check_health:
            self.check_health()

    def check_health(self) -> bool:
        """
        Checks the status of each health check.
        https://kairosdb.github.io/docs/restapi/Health.html#status
        :return: If all are healthy it returns True otherwise Exception is raised.
        """
        _url = f"{self.uri}{_cnsts.HEALTH_CHECK_API}"
        resp = rest_client.get(url=_url)
        if resp.status_code in _cnsts.SUCCESS_CODES:
            return True

    def check_health_status(self) -> list:
        """
        Returns the status of each health check as JSON.
        https://kairosdb.github.io/docs/restapi/Health.html#status
        :return:
        [The JVM thread deadlock check verifies that no deadlocks exist in the KairosDB JVM,
        The Datastore query check performs a query on the data store to ensure that the data store is responding.]
        """
        _url = f"{self.uri}{_cnsts.HEALTH_STATUS_API}"
        resp = rest_client.get(url=_url)
        if resp.status_code in _cnsts.SUCCESS_CODES:
            return resp.json()

    def features(self, feature: str = None):
        """
        The Features API returns metadata about various components of KairosDB.
        For example, this API will return metadata about aggregators and GroupBys.
        :param feature: To return metadata for a particular feature, include this parameter.
        :return: All features as a dictionary
        """
        _url = f"{self.uri}{_cnsts.FEATURES_API}"
        if feature:
            _url += f"/{feature}"
        resp = rest_client.get(url=_url)
        return resp.json()

    def get_metric_names(self, prefix: str = None) -> dict[str, list]:
        """
        Returns a list of all metric names.
        If you specify the prefix parameter, only names that start with prefix are returned.
        :param prefix: Prefix parameter
        :return: A list of metric names
        """
        _url = f"{self.uri}{_cnsts.METRIC_NAMES_API}"
        if prefix:
            _url += f"?prefix={prefix}"
        resp = rest_client.get(url=_url)
        return resp.json()

    def query(self, query: dict | Query, form_df: bool = False) -> dict | pandas.DataFrame:
        """
        Returns a list of metric values based on a set of criteria.
        Also returns a set of all tag names and values that are found across the data points.

        :param form_df: Set to true to output as a dataframe
        :param query: A query dictionary or a Query object
        :return: A Pandas DataFrame if form_df argument is true else a dictionary
        """
        _url = f"{self.uri}{_cnsts.QUERY_API}"
        if isinstance(query, Query):
            raise NotImplementedError("Feature is under development")
        if form_df:
            raise NotImplementedError("Feature is under development")
        resp = rest_client.post(url=_url, json=query)
        return resp.json()
