# ROOT: compose.yml - Main orchestration file
# This file defines the core platform infrastructure and shared networks

networks:
  traefik:
    external: false
    name: traefik
  database:
    external: false
    name: database
  internal:
    external: false
    name: internal

volumes:
  traefik_data:
    name: traefik_data
  nginx_data:
    name: nginx_data
  postgres_data:
    name: postgres_data
  redis_data:
    name: redis_data
  rabbitmq_data:
    name: rabbitmq_data
  platform_logs:
    name: platform_logs

services:
  # Load Balancer / Reverse Proxy
  traefik:
    extends:
      file: ./domains/core/traefik/compose.yml
      service: traefik
    networks:
      - traefik
      - internal

  # Edge Gateway
  nginx:
    extends:
      file: ./domains/core/nginx/compose.yml
      service: nginx
    networks:
      - traefik
    depends_on:
      - traefik

  # Container Updates
  watchtower:
    extends:
      file: ./domains/core/watchtower/compose.yml
      service: watchtower
    networks:
      - internal

  # Health Monitoring
  healthchecks:
    extends:
      file: ./domains/core/healthchecks/compose.yml
      service: healthchecks
    networks:
      - traefik
      - database
    depends_on:
      - postgresql

  # Database Services
  postgresql:
    extends:
      file: ./domains/data/postgresql/compose.yml
      service: postgresql
    networks:
      - database

  redis:
    extends:
      file: ./domains/data/redis/compose.yml
      service: redis
    networks:
      - database

  rabbitmq:
    extends:
      file: ./domains/data/rabbitmq/compose.yml
      service: rabbitmq
    networks:
      - database
      - traefik

---

# domains/core/traefik/compose.yml
services:
  traefik:
    image: traefik:v3.1
    container_name: traefik
    restart: unless-stopped
    command:
      - "--api.dashboard=true"
      - "--api.debug=true"
      - "--log.level=INFO"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--providers.docker.network=traefik"
      - "--providers.file.directory=/etc/traefik/dynamic"
      - "--providers.file.watch=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--entrypoints.web.http.redirections.entrypoint.to=websecure"
      - "--entrypoints.web.http.redirections.entrypoint.scheme=https"
      - "--certificatesresolvers.letsencrypt.acme.email=admin@localhost"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge=true"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
      - "--metrics.prometheus=true"
      - "--accesslog=true"
      - "--accesslog.filepath=/var/log/traefik/access.log"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - traefik_data:/letsencrypt
      - ./config/traefik/dynamic:/etc/traefik/dynamic:ro
      - platform_logs:/var/log/traefik
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.traefik.rule=Host(`traefik.localhost`)"
      - "traefik.http.routers.traefik.entrypoints=websecure"
      - "traefik.http.routers.traefik.tls.certresolver=letsencrypt"
      - "traefik.http.routers.traefik.service=api@internal"
      - "traefik.http.middlewares.traefik-auth.basicauth.users=admin:$$2y$$10$$8qkAP0B9AjQjK0xGw0Hq5uGHvJwE3UG5zEtN1wJnKr8vL.Lq9K8qK"
      - "traefik.http.routers.traefik.middlewares=traefik-auth"
      - "platform.domain=core"
      - "platform.service=traefik"
    environment:
      - TRAEFIK_LOG_LEVEL=INFO
    healthcheck:
      test: ["CMD", "traefik", "healthcheck"]
      interval: 30s
      timeout: 10s
      retries: 3

---

# domains/core/nginx/compose.yml
services:
  nginx:
    image: nginx:alpine
    container_name: nginx
    restart: unless-stopped
    volumes:
      - ./config/nginx/conf.d:/etc/nginx/conf.d:ro
      - ./config/nginx/html:/usr/share/nginx/html:ro
      - ./config/nginx/certs:/etc/nginx/certs:ro
      - platform_logs:/var/log/nginx
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.nginx.rule=Host(`platform.localhost`)"
      - "traefik.http.routers.nginx.entrypoints=websecure"
      - "traefik.http.routers.nginx.tls.certresolver=letsencrypt"
      - "traefik.http.services.nginx.loadbalancer.server.port=80"
      - "platform.domain=core"
      - "platform.service=nginx"
      - "platform.description=Platform Homepage and Edge Gateway"
    healthcheck:
      test: ["CMD", "nginx", "-t"]
      interval: 30s
      timeout: 10s
      retries: 3
    depends_on:
      - traefik

---

# domains/core/watchtower/compose.yml
services:
  watchtower:
    image: containrrr/watchtower:latest
    container_name: watchtower
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - platform_logs:/logs
    environment:
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_INCLUDE_RESTARTING=true
      - WATCHTOWER_SCHEDULE=0 0 2 * * *  # 2 AM daily
      - WATCHTOWER_NOTIFICATIONS=email
      - WATCHTOWER_NOTIFICATION_EMAIL_FROM=watchtower@localhost
      - WATCHTOWER_NOTIFICATION_EMAIL_TO=admin@localhost
      - WATCHTOWER_NOTIFICATION_EMAIL_SERVER=mailserver
      - WATCHTOWER_NOTIFICATION_EMAIL_SERVER_PORT=587
      - WATCHTOWER_LOG_LEVEL=info
    labels:
      - "platform.domain=core"
      - "platform.service=watchtower"
      - "platform.description=Automated Container Updates"
    command: --interval 86400 --cleanup --include-restarting

---

# domains/core/healthchecks/compose.yml
services:
  healthchecks:
    image: healthchecks/healthchecks:latest
    container_name: healthchecks
    restart: unless-stopped
    environment:
      - SECRET_KEY=your-secret-key-change-this
      - DEBUG=False
      - DEFAULT_FROM_EMAIL=healthchecks@localhost
      - EMAIL_HOST=mailserver
      - EMAIL_PORT=587
      - EMAIL_USE_TLS=True
      - ALLOWED_HOSTS=healthchecks.localhost,localhost
      - SITE_ROOT=https://healthchecks.localhost
      - SITE_NAME=Platform Health Checks
      - DB_HOST=postgresql
      - DB_PORT=5432
      - DB_NAME=healthchecks
      - DB_USER=healthchecks
      - DB_PASSWORD=healthchecks_password
    volumes:
      - platform_logs:/app/logs
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.healthchecks.rule=Host(`healthchecks.localhost`)"
      - "traefik.http.routers.healthchecks.entrypoints=websecure"
      - "traefik.http.routers.healthchecks.tls.certresolver=letsencrypt"
      - "traefik.http.services.healthchecks.loadbalancer.server.port=8000"
      - "platform.domain=core"
      - "platform.service=healthchecks"
      - "platform.description=Service Health Monitoring"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
    depends_on:
      - postgresql

---

# domains/data/postgresql/compose.yml
services:
  postgresql:
    image: postgres:16-alpine
    container_name: postgresql
    restart: unless-stopped
    environment:
      - POSTGRES_DB=platform
      - POSTGRES_USER=platform
      - POSTGRES_PASSWORD=platform_secure_password
      - POSTGRES_MULTIPLE_DATABASES=healthchecks,grafana,n8n
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./config/postgresql/init:/docker-entrypoint-initdb.d:ro
      - platform_logs:/var/log/postgresql
    labels:
      - "platform.domain=data"
      - "platform.service=postgresql"
      - "platform.description=Primary Database Service"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U platform -d platform"]
      interval: 30s
      timeout: 10s
      retries: 5
    ports:
      - "127.0.0.1:5432:5432"  # Only accessible from localhost

---

# domains/data/redis/compose.yml
services:
  redis:
    image: redis:7-alpine
    container_name: redis
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass redis_secure_password
    volumes:
      - redis_data:/data
      - platform_logs:/var/log/redis
    labels:
      - "platform.domain=data"
      - "platform.service=redis"
      - "platform.description=In-Memory Cache and Session Store"
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
    ports:
      - "127.0.0.1:6379:6379"  # Only accessible from localhost

---

# domains/data/rabbitmq/compose.yml
services:
  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: rabbitmq
    restart: unless-stopped
    environment:
      - RABBITMQ_DEFAULT_USER=platform
      - RABBITMQ_DEFAULT_PASS=rabbitmq_secure_password
      - RABBITMQ_DEFAULT_VHOST=platform
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
      - platform_logs:/var/log/rabbitmq
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.rabbitmq.rule=Host(`rabbitmq.localhost`)"
      - "traefik.http.routers.rabbitmq.entrypoints=websecure"
      - "traefik.http.routers.rabbitmq.tls.certresolver=letsencrypt"
      - "traefik.http.services.rabbitmq.loadbalancer.server.port=15672"
      - "platform.domain=data"
      - "platform.service=rabbitmq"
      - "platform.description=Message Queue and Event Streaming"
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
    ports:
      - "127.0.0.1:5672:5672"   # AMQP port - localhost only
      - "127.0.0.1:15672:15672" # Management UI - localhost only