# Certificate Policy

This policy defines certificate requirements per environment and the resulting behavior.

## Environments
- Production: organization-approved certificates only (internal PKI or CA-signed)
- Non-Production (dev, lab/staging on isolated networks): self-signed allowed

## Validation Rules
- Expiry: certificates must be valid (not expired)
- Chain: full chain must be present and valid
- Policy: self-signed forbidden in production

## Exposure Behavior
- Invalid/missing certificates: withhold exposure for the affected endpoint
- Emit AuditEvent(policy_violation) with reason and service identifier
- Other services remain available

## Renewal Guidance
- Use automated renewal where possible for non-dev environments
- Track expiration and alert at 30/7/1 days
