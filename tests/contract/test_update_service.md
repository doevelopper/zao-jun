# Contract Test: Update Service Metadata (Failing Spec)

Ref: specs/001-modular-container-platform/contracts/platform-contracts.md (Update Service Metadata)

## Preconditions
- Existing service in catalog
- Proposed changes do not violate uniqueness constraints

## Expected Behavior
- Validate delta; apply changes; update homepage; record audit event

## Negative Cases
- Route/name conflicts introduced: reject with actionable error
- Attempt to expose host port: reject, record policy_violation audit event

## Assertions (to be automated)
- returns: { success: false, error: "route-conflict" } when conflicting route
- returns: { success: false, error: "name-conflict" } when duplicate name
- returns: { success: false, error: "policy-violation" } on direct port exposure attempt
- returns: { success: true } and emits AuditEvent(update) on success

Status: FAILING (no implementation yet)
