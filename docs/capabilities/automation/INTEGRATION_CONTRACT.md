# Automation Integration Contract

## Safety Capability

Hosts may supply a `SafetyGateway` implementing `assess(context)` and `recover(context, error)`. Assessment returns allow/deny, risk level, approval requirement, and reason. Automation never bypasses a denied decision or a required user approval.

## Enhancement Capability

Hosts may supply an `EnhancementGateway` implementing `insights(context)`. Returned Analytics, Pattern Analysis, Optimization, and Rule Generation results are advisory inputs. Auto Decision may recommend a candidate, but application authority remains governed by the configured approval policy.

## Collaboration & Connectivity Capability

`AutomationRuntime` accepts an optional `CollaborationGateway`. An approved `auto_execute` payload may include `connector_request`; the runtime passes it to `execute_connector_request` during the Execution stage and records the provider-neutral response. Without a configured gateway the request fails safely. Connector execution still performs its own Safety validation and execution recording.

## Project boundary

Living OS, Universal Learning Engine, and future projects submit public requests and decide how successful results map to their own operations. No project runtime or database is imported by this package.

