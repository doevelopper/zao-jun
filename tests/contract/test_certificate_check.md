# Contract Test: Certificate Check (Failing Spec)

Ref: specs/001-modular-container-platform/contracts/platform-contracts.md (Certificate Check)

## Preconditions
- Endpoint has certificate material associated with environment

## Expected Behavior
- Validate against environment policy; expose or withhold accordingly
- Emit audit event for invalid/missing certificates

## Negative Cases
- Expired cert, missing chain, self-signed in production

## Assertions (to be automated)
- returns: { valid: false, reason: "expired" } for expired cert
- returns: { valid: false, reason: "missing-chain" } for incomplete chain
- returns: { valid: false, reason: "policy-violation" } for self-signed in production
- returns: { valid: true } for compliant cert
- emits AuditEvent(policy_violation) when invalid/missing

Status: FAILING (no implementation yet)
