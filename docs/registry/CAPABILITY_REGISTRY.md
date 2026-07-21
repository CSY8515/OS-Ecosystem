# Capability Registry

Version: v0.6.0

| Capability | Version | Status | Documentation |
| --- | --- | --- | --- |
| Safety | v1.0.0 | Stable | [Safety](../capabilities/safety/README.md) |
| Enhancement | v1.0.0 | Stable | [Enhancement](../capabilities/enhancement/README.md) |
| Automation | v1.0.0 | Stable | [Automation](../capabilities/automation/README.md) |
| Collaboration & Connectivity | v1.0.0 | Stable | [Collaboration & Connectivity](../capabilities/collaboration-connectivity/README.md) |
| Personal Secretary | v1.0.0 | Stable | [Personal Secretary](../capabilities/personal-secretary/README.md) |

Collaboration & Connectivity depends on Safety, Enhancement, and Automation contracts. It provides Connector Registry, Connection Contract, Import / Export, Data Transformation, Internal Messaging, Sync Foundation, Health Check, Failure Handling, and Execution Record.

Personal Secretary consumes project-owned snapshots and existing capability contracts to provide deterministic briefings, reviews, recommendations, reminders, priorities, decision support, and notifications. It remains advisory and has no AI dependency.

Implementations remain in existing code directories and follow the [Capability Documentation Standard](../capabilities/README.md).
