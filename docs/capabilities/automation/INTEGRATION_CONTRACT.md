# Automation Integration Contract

## Safety Capability

Hosts may supply a `SafetyGateway` implementing `assess(context)` and `recover(context, error)`. Assessment returns allow/deny, risk level, approval requirement, and reason. Automation never bypasses a denied decision or a required user approval.

## Enhancement Capability

Hosts may supply an `EnhancementGateway` implementing `insights(context)`. Returned Analytics, Pattern Analysis, Optimization, and Rule Generation results are advisory inputs. Auto Decision may recommend a candidate, but application authority remains governed by the configured approval policy.

## Project boundary

Living OS, Universal Learning Engine, and future projects submit public requests and decide how successful results map to their own operations. No project runtime or database is imported by this package.

