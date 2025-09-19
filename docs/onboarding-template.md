# Onboarding Template (≤ 10 minutes)

Use this checklist to onboard a new service quickly and safely.

## 1. Prepare Metadata
- [ ] Choose unique service `name`
- [ ] Select `domain` (or define it)
- [ ] Define `routes` (host/path rule). Ensure uniqueness
- [ ] Set `visibility` (public|restricted)
- [ ] Determine health check endpoint and initial `health`

## 2. Validate
- [ ] Check no duplicate name/route exists in catalog
- [ ] Confirm certificate policy for target environment
- [ ] Confirm RBAC domain access for intended viewers

## 3. Submit
- [ ] Submit metadata via onboarding channel
- [ ] Address validation errors if any; resubmit

## 4. Verify
- [ ] Homepage shows service under correct domain
- [ ] Status badge reflects health; link works over TLS
- [ ] Audit event recorded

Notes
- Direct host port exposure is prohibited
- Invalid/missing certificates block exposure for the affected endpoint
