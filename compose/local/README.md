# Zao-Jun Local Stack (Traefik + Sample Services)

This is a minimal local docker-compose stack to try the single-entry approach using Traefik (TLS on :443) and a few sample services that match the catalog routes.

## Prereqs
- Docker and Docker Compose
- Local DNS for .local hosts (e.g., add to /etc/hosts)

Add entries to /etc/hosts:

```
127.0.0.1  home.local traefik.local whoami.local nginx.local fider.local hc.local ollama.local openwebui.local confluence.local jira.local jira-core.local bitbucket.local crucible.local fisheye.local mcp.local youtrack.local jetbrains-hub.local qodana.local qodana-python.local qodana-clang.local qodana-cpp.local n8n.local
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
- Ollama API: https://ollama.local
- Open WebUI: https://openwebui.local
 - n8n: https://n8n.local
 - Confluence: https://confluence.local
 - Jira Software: https://jira.local
 - Jira Core: https://jira-core.local
 - Bitbucket: https://bitbucket.local
 - Crucible: https://crucible.local
 - Fisheye: https://fisheye.local
 - MCP (placeholder): https://mcp.local
 - YouTrack: https://youtrack.local
 - JetBrains Hub: https://jetbrains-hub.local
 - Qodana (generic): https://qodana.local
 - Qodana Python: https://qodana-python.local
 - Qodana Clang: https://qodana-clang.local
 - Qodana C++: https://qodana-cpp.local

Qodana note: These services are placeholders and won’t start by default. Enable with the `qodana` profile and mount your project into `/data/project`, then replace the `command` with your desired Qodana run. Example:

```
docker compose --profile qodana up -d qodana_python
# then exec into the container and run qodana CLI as needed
```

Note: Certificates are self-signed. Your browser will show a warning unless you trust them. For trusted local certs, consider mkcert, or wire real certificates.

GPU note: The provided Open WebUI image tag is `:cuda` and supports GPU acceleration with Ollama if your host has NVIDIA drivers and Docker GPU support. You may need to uncomment the `deploy.resources.reservations.devices` block in `docker-compose.yml` under `ollama` or run Docker with `--gpus all`.

## Data directories

- Ollama models/cache: `compose/local/data/ollama`
- Open WebUI data: `compose/local/data/openwebui`
 - Postgres data: `compose/local/data/postgres`
 - n8n data: `compose/local/data/n8n`

Note: Models can be large (several GB); ensure you have available disk. These paths are git-ignored.

## Postgres defaults (dev only)

- Host: postgres
- Port: 5432
- User/Password: `zaojun`/`zaojun`
- DBs pre-created: `youtrack`, `hub`, `n8n`

YouTrack and Hub are set to use the external Postgres; expect initial setup screens to confirm DB and admin user.

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
