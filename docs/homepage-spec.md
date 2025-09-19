# Homepage Specification

## Purpose
Provide a centralized entry point for discovering services by domain with clear health status and access links.

## Grouping
- Group services by Domain.name
- Within a domain, sort by service name

## Status Badges
- healthy: green badge, link enabled
- degraded: yellow/orange badge, link enabled
- unavailable: red badge, link disabled, tooltip/reason shown

## Entries
- Show: name, optional icon/label, status badge, link (URL)
- Restricted services: hide or show based on viewer’s access (RBAC/GBAC)

## Behavior
- Updates reflect routing/health changes without manual platform restarts
- Large catalogs: provide pagination or grouping when >100 services
