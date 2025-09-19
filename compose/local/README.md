# Zao-Jun Local Stack (Traefik + Sample Services)

This is a minimal local docker-compose stack to try the single-entry approach using Traefik (TLS on :443) and a few sample services that match the catalog routes.

## Prereqs
- Docker and Docker Compose
- Local DNS for .local hosts (e.g., add to /etc/hosts)

Add entries to /etc/hosts:

```
127.0.0.1  home.local traefik.local whoami.local nginx.local fider.local hc.local
```

Optional: add more from your catalog, e.g. `grafana.local`, `n8n.local`, etc.

## Start stack

```
cd compose/local
docker compose up -d
```

- Traefik dashboard: https://traefik.local:443 (self-signed)
- Homepage placeholder: https://home.local
- WhoAmI: https://whoami.local
- NGINX: https://nginx.local
- Fider: https://fider.local
- Healthchecks: https://hc.local

Note: Certificates are self-signed. Your browser will show a warning unless you trust them. For trusted local certs, consider mkcert, or wire real certificates.

## Use generated homepage
You can replace the placeholder content with your generated homepage:

```
# from repo root
cp specs/001-modular-container-platform/catalog/homepage.html compose/local/homepage/index.html
```

Then refresh https://home.local

## Map more services
Follow the pattern in `docker-compose.yml` to add labels for each service:

```
labels:
  - traefik.enable=true
  - traefik.http.routers.SVC.rule=Host(`HOSTNAME.local`)
  - traefik.http.routers.SVC.entrypoints=websecure
  - traefik.http.routers.SVC.tls=true
  - traefik.http.services.SVC.loadbalancer.server.port=PORT
```

Replace SVC, HOSTNAME, and PORT accordingly.
