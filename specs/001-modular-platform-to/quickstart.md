# Quickstart – Modular Multi-Service Platform

## Goal
Demonstrate registering a service, verifying routing & certificate status, and viewing dashboard status feed.

## Prerequisites
- Running platform stack (gateway, router, Postgres, health aggregator, dashboard assets).
- CLI tools: curl, openssl (for certificate inspection).

## Steps
1. Register a Service
```
POST /services
{
  "service_name": "demo-api",
  "owner_contact": "team-platform",
  "primary_domain": "demo.local",
  "container_image_ref": "registry/demo-api:sha256-abc",
  "business_purpose": "Demonstration endpoint",
  "support_channel": "#platform-support",
  "compliance_tier": "standard",
  "requested_cert_type": "self-signed",
  "health_check_path": "/healthz",
  "category": "Automation"
}
```
2. Poll Onboarding Status
```
GET /services?status=Onboarding
```
3. Confirm Healthy Transition
```
GET /services?status=Healthy&category=Automation
```
4. Inspect Status Feed
```
GET /status/services.json
```
5. Preview Domain Change
```
POST /routing/preview { "proposed_rules": [{"domain":"demo2.local","path_pattern":"/","service_id":"<id>"}] }
```
6. Reassign Domain (if preview clean)
```
POST /services/<id>/domain { "primary_domain": "demo2.local" }
```
7. View Dashboard
Navigate to: https://<gateway-host>/ (dashboard lists demo-api with Healthy status)

8. Check Certificate Days to Expiry
```
GET /services/<id>/certificate  # (future endpoint for metadata)
```

## Expected Outcomes
- Service transitions to Healthy within SLA.
- Dashboard lists service with correct category and status.
- Status feed includes service with latency and error placeholders (0 if idle).
- Preview prevents conflicting domain claims.

## Cleanup
```
POST /services/<id>/decommission
```

**Status**: Draft – aligns with FR-001..FR-015, FR-021..FR-028.
