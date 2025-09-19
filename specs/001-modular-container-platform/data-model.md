# Data Model

Entities derived from the feature specification.

## Service
- name: string (unique)
- domain: string (references Domain.name)
- routes: list<Route> (at least one)
- health: enum { healthy, degraded, unavailable }
- visibility: enum { public, restricted }
- metadata: map<string,string>

## Domain
- name: string (unique)
- description: string
- accessGroups: list<string> (authorization mapping)

## Route
- rule: string (unique across platform; host/path expression)
- serviceName: string (references Service.name)
- enabled: boolean

## HomepageEntry
- serviceName: string (references Service.name)
- label: string
- status: enum { healthy, degraded, unavailable }
- link: string (URL)

## AuditEvent
- id: string (unique)
- type: enum { create, update, remove, policy_violation }
- actor: string
- timestamp: datetime
- details: map<string,string>

## UserType (role)
- name: enum { PlatformAdmin, ServiceOwner, Viewer }
- permissions: list<string>
