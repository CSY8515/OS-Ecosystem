"""Collaboration & Connectivity Capability v1.0.0 public API."""

from .connector import BaseConnector, InMemoryConnector
from .contracts import AutomationConnectorGateway, EnhancementGateway, SafetyAssessment, SafetyGateway
from .enums import ConnectorStatus, ConnectorType, ErrorCode, HealthStatus, MessageStatus, SyncStatus
from .errors import CollaborationConnectivityError, UnsupportedOperationError
from .execution import ExecutionRecorder
from .import_export import export_data, import_data
from .messaging import InMemoryMessageBus
from .models import (
    CAPABILITY_VERSION,
    CollaborationConnectivityExecutionRecord,
    CollaborationMessage,
    ConnectionRequest,
    ConnectionResponse,
    ConnectorHealthResult,
    ConnectorMetadata,
    ExportRequest,
    ExportResult,
    ImportRequest,
    ImportResult,
    MessageResult,
    RetryPolicy,
    SyncRecord,
    SyncRequest,
    TransformationResult,
    TransformationRule,
)
from .registry import ConnectorRegistry
from .service import CollaborationConnectivityService, DefaultSafetyGateway, NullEnhancementGateway
from .synchronization import SynchronizationManager
from .transformation import transform_record

__version__ = CAPABILITY_VERSION

__all__ = [
    "CAPABILITY_VERSION", "AutomationConnectorGateway", "BaseConnector", "CollaborationConnectivityError",
    "CollaborationConnectivityExecutionRecord", "CollaborationConnectivityService", "CollaborationMessage",
    "ConnectionRequest", "ConnectionResponse", "ConnectorHealthResult", "ConnectorMetadata", "ConnectorRegistry",
    "ConnectorStatus", "ConnectorType", "DefaultSafetyGateway", "EnhancementGateway", "ErrorCode", "ExecutionRecorder",
    "ExportRequest", "ExportResult", "HealthStatus", "ImportRequest", "ImportResult", "InMemoryConnector",
    "InMemoryMessageBus", "MessageResult", "MessageStatus", "NullEnhancementGateway", "RetryPolicy", "SafetyAssessment",
    "SafetyGateway", "SyncRecord", "SyncRequest", "SyncStatus", "SynchronizationManager", "TransformationResult",
    "TransformationRule", "UnsupportedOperationError", "export_data", "import_data", "transform_record",
]
