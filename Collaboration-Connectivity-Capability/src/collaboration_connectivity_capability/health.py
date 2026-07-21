"""Connector health aggregation."""

from .enums import HealthStatus
from .models import ConnectorHealthResult
from .registry import ConnectorRegistry


def check_all(registry: ConnectorRegistry) -> dict[str, ConnectorHealthResult]:
    return {metadata.connector_id: registry.get(metadata.connector_id).health_check() for metadata in registry.list_connectors()}


def overall_status(results: dict[str, ConnectorHealthResult]) -> HealthStatus:
    statuses = {result.status for result in results.values()}
    if not statuses:
        return HealthStatus.UNKNOWN
    if statuses <= {HealthStatus.HEALTHY, HealthStatus.DISABLED} and HealthStatus.HEALTHY in statuses:
        return HealthStatus.HEALTHY
    if HealthStatus.UNHEALTHY in statuses:
        return HealthStatus.UNHEALTHY
    return HealthStatus.DEGRADED
