# Quickstart

This quickstart demonstrates the happy path from template to exposed service under the platform’s constraints.

1. Prepare Service Metadata
- Choose a unique service name and routes (host/path rules)
- Select a domain (or create one with description and access groups)
- Determine visibility and health check endpoint

2. Validate Locally
- Ensure no duplicate name or routes against current catalog
- Verify certificate policy for the target environment

3. Submit Onboarding
- Provide metadata via the designated onboarding channel
- Observe validation; fix any conflicts and resubmit

4. Confirm Exposure
- Once healthy, the service appears on the homepage with status
- Verify link works over TLS via the single entry point

5. Update / Remove
- Changes follow the same validation and audit process
- Removal cleans up routes and homepage entry

Notes
- Onboarding target: < 10 minutes for a trained user
- Invalid/missing certificates block exposure for the affected endpoint
- Direct host port exposure is prohibited and will be blocked + audited
