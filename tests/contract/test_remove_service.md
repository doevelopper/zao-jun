# Contract Test: Remove Service (Failing Spec)

Ref: specs/001-modular-container-platform/contracts/platform-contracts.md (Remove Service)

## Preconditions
- Existing service in catalog

## Expected Behavior
- Remove routes and homepage entry; record audit event

## Negative Cases
- Service not found: return specific error

## Assertions (to be automated)
- returns: { success: false, error: "not-found" } when service is missing
- returns: { success: true } and emits AuditEvent(remove) on success
- homepage no longer lists the service

Status: FAILING (no implementation yet)
