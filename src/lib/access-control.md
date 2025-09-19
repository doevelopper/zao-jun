# Access Control

Access control is enforced via authentication (SSO) and authorization (RBAC/GBAC) mapped to domains.

## Authentication
- Use the organization Identity Provider (SSO) for user identity
- Sessions/tokens must be validated by the edge before access is granted

## Authorization
- Roles: PlatformAdmin, ServiceOwner, Viewer
- Domain Mappings:
  - PlatformAdmin: full access to all domains and audit logs
  - ServiceOwner: manage services only in assigned domains
  - Viewer: read-only access to permitted domains

## Least Privilege
- Grant the minimal set of permissions needed
- Review mappings regularly; remove stale group assignments

## Policy Violations
- Attempts to bypass access controls must be rejected and audited
