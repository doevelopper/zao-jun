# Platform Contracts (Conceptual)

This document captures high-level contracts implied by user actions. Implementation details are intentionally omitted per constitution.

## Contract: Onboard Service
- Input metadata: { name, domain, routes[], visibility, healthCheck }
- Pre-conditions: unique name; unique routes; certificate policy satisfied (for intended environment)
- Output: service listed on homepage (pending healthy), routing active; audit event recorded
- Errors: conflicts detected; invalid metadata; certificate invalid/missing (exposure withheld)

## Contract: Update Service Metadata
- Input metadata delta: { name?, domain?, routes?, visibility? }
- Effects: validation; apply changes; update homepage status; audit event recorded
- Errors: conflicts; invalid values; attempt to expose host port is blocked (policy_violation)

## Contract: Remove Service
- Input: service identifier (name)
- Effects: remove routes; remove homepage entry; audit event recorded
- Errors: service not found; dependency constraints

## Contract: View Homepage
- Input: none
- Output: list of services grouped by domain with { name, status, link }
- Errors: none (page may indicate degraded statuses)

## Contract: Certificate Check
- Input: endpoint certificate for service
- Effects: validate against environment policy; expose or withhold
- Output: audit event on invalid/missing
- Errors: invalid cert, expired cert, missing chain
