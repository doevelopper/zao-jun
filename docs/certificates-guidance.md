# Certificates Guidance

Summary of certificate sources and allowed usage by environment.

## Production
- Allowed: organization-approved certificates (internal PKI or public CA)
- Not allowed: self-signed certificates
- Recommendation: automated renewal, monitored expiry alerts (30/7/1 days)

## Non-Production (Dev, Lab/Staging on isolated networks)
- Allowed: self-signed certificates
- Recommendation: document generation process and distribution to clients where needed

## Troubleshooting
- If exposure withheld: check expiry, chain, and environment policy
- Audit logs contain reasons for policy violations
