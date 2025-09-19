# Audit Events

Audit events provide an immutable trail of significant actions and policy enforcement.

## Event Types
- create: service onboarded
- update: service metadata changed
- remove: service removed
- policy_violation: attempt blocked (e.g., direct port exposure, invalid certificate)

## Required Fields
- id: unique identifier (string)
- type: one of the event types above
- actor: who initiated the action
- timestamp: ISO 8601 date-time
- details: key/value map with context (e.g., service name, route, reason)

## Emission Rules
- Emit exactly one event per accepted change
- Emit policy_violation on rejected actions that breach policies
- Events must be stored in an append-only log
