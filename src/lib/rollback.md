# Rollback

Guidance for reverting configuration changes that degrade availability.

## Triggers
- New configuration causes service unavailability
- Validation errors discovered post-activation
- Security or policy violations detected after change

## Steps
1. Identify last known-good state (previous validated catalog/config)
2. Revert to last known-good atomically (all-or-nothing)
3. Verify service availability and routing
4. Record AuditEvent(update) with rollback=true

## Notes
- Keep a rolling history of validated configurations for fast restore
- Prefer automated rollback where safe; manual approval for production
