# Observability

Baseline observability requirements for the platform and exposed services.

## Logging
- Structured logs (JSON preferred) with context: timestamp, level, service, request id
- Central aggregation with minimum 14-day retention (90 days recommended)
- Access logs for the edge entry point must be retained

## Metrics
- Collect system and service metrics at ≤60s intervals
- Core metrics: availability, latency, error rates, CPU/memory utilization
- Provide basic dashboards to visualize trends

## Alerts (Guidance)
- Alert on sustained unavailability or error spikes
- Alert on certificate expiry windows (30/7/1 days)

## Tracing (Optional)
- Where feasible, correlate requests via request id and trace context
