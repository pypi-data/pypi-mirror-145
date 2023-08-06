import pkg_resources
from typing import List

from rest_clients.abstract_client import AbstractClient
from s4f_clients.service_health_status import HealthStatusClient
from sql_client import SQLClient
from sql_client.sql_client import DatabaseNotConfigured

from stock_service.config import OldConfig
from stock_service.utils.db import ConnectionType
from stock_service.utils.stats import profile_with_stats

SQL_CLIENT = OldConfig.get_db_client()


def get_service_status():
    """
    Returns the status of the service. Status is determined by whether the service is running or not
    :return:
    """
    version = pkg_resources.get_distribution("stock-service").version
    return {"ok": True, "version": version}


@profile_with_stats(namespace="health")
def get_downstream_services_status(
    http_downstreams: List[AbstractClient] = [], s4f_downstreams: List[str] = []
) -> List[dict]:
    """
    gets status of down stream services stock-service depends on
        * master/slave take2 databases
        * http services
        * s4f services

    :param http_downstreams: list of http client
    :param s4f_downstreams: list of s4f host details
    """
    status_summary = []

    # get database status
    status_summary.extend(
        [
            get_database_status(SQL_CLIENT, ConnectionType.WRITE.value),
            get_database_status(SQL_CLIENT, ConnectionType.READ.value),
        ]
    )
    # http services status
    status_summary.extend(get_http_services_status(http_downstreams))
    # s4f services status
    status_summary.extend(get_s4f_services_status(s4f_downstreams))

    return status_summary


@profile_with_stats(namespace="health")
def get_http_services_status(http_clients: List) -> List[dict]:
    """
    gets the health status of http clients in http_downstreams
    :returns: list of dictionaries containing {'name', 'passed', 'message'}
    """
    status_summary = []
    for http_downstream in http_clients:
        service_name = http_downstream["client"].service_name
        service_status = {"name": service_name}
        try:
            service_response = http_downstream["client"].get_service_status()
        except Exception as e:
            service_status["passed"] = False
            service_status[
                "message"
            ] = f"Could not connect to http service {service_name}: {e}"
        else:
            service_status["passed"] = service_response["ok"]
            service_status[
                "message"
            ] = f"Successfully connected to http service: {service_name}"
        status_summary.append(service_status)
    return status_summary


@profile_with_stats(namespace="health")
def get_s4f_services_status(s4f_service: List[str]) -> List[dict]:
    """
    gets the health status of http clients in http_downstreams
    :returns: list of dictionaries containing {'name', 'passed', 'message'}
    """
    status_summary = []
    for service_name in s4f_service:
        service_status = {"name": service_name}
        try:
            client = HealthStatusClient(endpoints=OldConfig.find_service(service_name))
            service_status["passed"] = client.get_service_status().ok
        except Exception as e:
            service_status["passed"] = False
            service_status[
                "message"
            ] = f"Could not connect to s4f service {service_name}: {e}"
        else:
            service_status[
                "message"
            ] = f"Successfully connected to s4f service: {service_name}"
        status_summary.append(service_status)
    return status_summary


@profile_with_stats(namespace="health")
def get_database_status(sqlclient: SQLClient, role: str) -> dict:
    """
    returns db status as dict using sqlclient
    :param sqlclient: tal sql client instance
    :param role: configured role name
    """
    try:
        is_connected = sqlclient.verify_connection(role)
    except DatabaseNotConfigured:
        is_connected = False

    url = str(sqlclient.get_engine(role))
    if is_connected:
        message = f"connection to database successful: {url}"
    else:
        message = f"could not connect to database: {url}"
    return dict(passed=is_connected, message=message, name=url)
