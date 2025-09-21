# config/traefik/dynamic/tls.yml
tls:
  options:
    default:
      sslProtocols:
        - "TLSv1.2"
        - "TLSv1.3"
      cipherSuites:
        - "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"
        - "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305"
        - "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"

http:
  middlewares:
    secure-headers:
      headers:
        accessControlAllowMethods:
          - GET
          - OPTIONS
          - PUT
        accessControlMaxAge: 100
        hostsProxyHeaders:
          - "X-Forwarded-Host"
        referrerPolicy: "same-origin"
        customRequestHeaders:
          X-Forwarded-Proto: "https"
        customResponseHeaders:
          X-Frame-Options: "SAMEORIGIN"
          X-Content-Type-Options: "nosniff"
          X-XSS-Protection: "1; mode=block"
          Strict-Transport-Security: "max-age=31536000; includeSubDomains"

---

# config/nginx/conf.d/default.conf
upstream traefik_backend {
    server traefik:80;
}

server {
    listen 80;
    server_name platform.localhost;
    
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ =404;
    }
    
    location /api/ {
        proxy_pass http://traefik_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}

---

# config/nginx/html/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modular Container Platform</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .service-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        .service-card:hover {
            transform: translateY(-5px);
        }
        
        .service-card h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .service-status {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .status-healthy {
            background: #d4edda;
            color: #155724;
        }
        
        .status-unhealthy {
            background: #f8d7da;
            color: #721c24;
        }
        
        .service-link {
            display: inline-block;
            background: #667eea;
            color: white;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 5px;
            transition: background 0.3s ease;
        }
        
        .service-link:hover {
            background: #5a6fd8;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Modular Container Platform</h1>
            <p>Unified edge gateway with dynamic routing and rapid service deployment</p>
        </div>
        
        <div class="services-grid" id="services-grid">
            <!-- Services will be dynamically loaded here -->
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="total-services">0</div>
                <div class="stat-label">Total Services</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="healthy-services">0</div>
                <div class="stat-label">Healthy Services</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="platform-uptime">0d</div>
                <div class="stat-label">Platform Uptime</div>
            </div>
        </div>
    </div>

    <script>
        // Mock service data - in production, this would come from an API
        const services = [
            {
                name: 'Traefik Dashboard',
                description: 'Load balancer and reverse proxy',
                url: 'https://traefik.localhost',
                status: 'healthy',
                domain: 'core'
            },
            {
                name: 'Health Checks',
                description: 'Service health monitoring',
                url: 'https://healthchecks.localhost',
                status: 'healthy',
                domain: 'core'
            },
            {
                name: 'RabbitMQ Management',
                description: 'Message queue management',
                url: 'https://rabbitmq.localhost',
                status: 'healthy',
                domain: 'data'
            }
        ];

        function renderServices() {
            const grid = document.getElementById('services-grid');
            grid.innerHTML = services.map(service => `
                <div class="service-card">
                    <h3>${service.name}</h3>
                    <span class="service-status status-${service.status}">
                        ${service.status.toUpperCase()}
                    </span>
                    <p>${service.description}</p>
                    <br>
                    <small>Domain: ${service.domain}</small>
                    <br><br>
                    <a href="${service.url}" class="service-link" target="_blank">Access Service</a>
                </div>
            `).join('');
        }

        function updateStats() {
            document.getElementById('total-services').textContent = services.length;
            document.getElementById('healthy-services').textContent = 
                services.filter(s => s.status === 'healthy').length;
            
            // Mock uptime calculation
            const uptime = Math.floor((Date.now() - new Date('2024-01-01')) / (1000 * 60 * 60 * 24));
            document.getElementById('platform-uptime').textContent = `${uptime}d`;
        }

        // Initialize dashboard
        renderServices();
        updateStats();

        // Auto-refresh every 30 seconds
        setInterval(() => {
            // In production, fetch real service status
            updateStats();
        }, 30000);
    </script>
</body>
</html>

---

# config/postgresql/init/01-databases.sql
-- Create databases for different services
CREATE DATABASE healthchecks;
CREATE DATABASE grafana;
CREATE DATABASE n8n;

-- Create users with appropriate permissions
CREATE USER healthchecks WITH PASSWORD 'healthchecks_password';
GRANT ALL PRIVILEGES ON DATABASE healthchecks TO healthchecks;

CREATE USER grafana WITH PASSWORD 'grafana_password';
GRANT ALL PRIVILEGES ON DATABASE grafana TO grafana;

CREATE USER n8n WITH PASSWORD 'n8n_password';
GRANT ALL PRIVILEGES ON DATABASE n8n TO n8n;

---

# templates/basic-service/compose.yml.template
services:
  ${SERVICE_NAME}:
    image: ${SERVICE_IMAGE}:${SERVICE_TAG:-latest}
    container_name: ${SERVICE_NAME}
    restart: unless-stopped
    environment:
      # Add your environment variables here
      - ENV_VAR_1=value1
      - ENV_VAR_2=value2
    volumes:
      # Add your volume mappings here
      - ${SERVICE_NAME}_data:/data
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.${SERVICE_NAME}.rule=Host(\`${SERVICE_DOMAIN}\`)"
      - "traefik.http.routers.${SERVICE_NAME}.entrypoints=websecure"
      - "traefik.http.routers.${SERVICE_NAME}.tls.certresolver=letsencrypt"
      - "traefik.http.services.${SERVICE_NAME}.loadbalancer.server.port=${SERVICE_PORT:-80}"
      - "platform.domain=${PLATFORM_DOMAIN}"
      - "platform.service=${SERVICE_NAME}"
      - "platform.description=${SERVICE_DESCRIPTION}"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:${SERVICE_PORT:-80}/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - traefik

volumes:
  ${SERVICE_NAME}_data:
    name: ${SERVICE_NAME}_data

networks:
  traefik:
    external: true

---

# templates/basic-service/README.md
# Basic Service Template

This template provides a standardized way to onboard new services to the platform.

## Usage

1. Copy this template to your service directory
2. Replace all `${VARIABLE}` placeholders with actual values
3. Customize the configuration as needed
4. Deploy using the platform scripts

## Required Variables

- `SERVICE_NAME`: Unique name for your service
- `SERVICE_IMAGE`: Docker image name
- `SERVICE_DOMAIN`: Domain where service will be accessible
- `PLATFORM_DOMAIN`: Platform domain category (core, data, etc.)
- `SERVICE_DESCRIPTION`: Brief description of the service

## Optional Variables

- `SERVICE_TAG`: Image tag (defaults to latest)
- `SERVICE_PORT`: Internal port (defaults to 80)

## Example

```bash
export SERVICE_NAME=myapp
export SERVICE_IMAGE=myorg/myapp
export SERVICE_DOMAIN=myapp.localhost
export PLATFORM_DOMAIN=applications
export SERVICE_DESCRIPTION="My awesome application"

./scripts/deploy.sh ./domains/applications/myapp/
```

---

# scripts/deploy.sh
#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PLATFORM_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="${PLATFORM_ROOT}/logs"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Logging
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "${LOG_DIR}/deploy_${TIMESTAMP}.log"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "${LOG_DIR}/deploy_${TIMESTAMP}.log"
    exit 1
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "${LOG_DIR}/deploy_${TIMESTAMP}.log"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "${LOG_DIR}/deploy_${TIMESTAMP}.log"
}

# Help function
show_help() {
    cat << EOF
Platform Service Deployment Script

Usage: $0 [OPTIONS] SERVICE_PATH

Arguments:
    SERVICE_PATH    Path to service directory containing compose.yml

Options:
    -h, --help      Show this help message
    -c, --check     Perform pre-deployment checks only
    -v, --verbose   Enable verbose output
    -d, --dry-run   Show what would be deployed without executing

Examples:
    $0 ./domains/core/nginx/
    $0 --check ./domains/data/postgresql/
    $0 --dry-run ./domains/applications/myapp/

EOF
}

# Parse arguments
CHECK_ONLY=false
VERBOSE=false
DRY_RUN=false
SERVICE_PATH=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -c|--check)
            CHECK_ONLY=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            if [[ -z "$SERVICE_PATH" ]]; then
                SERVICE_PATH="$1"
            else
                error "Unknown argument: $1"
            fi
            shift
            ;;
    esac
done

# Validate inputs
if [[ -z "$SERVICE_PATH" ]]; then
    error "Service path is required. Use -h for help."
fi

if [[ ! -d "$SERVICE_PATH" ]]; then
    error "Service directory does not exist: $SERVICE_PATH"
fi

if [[ ! -f "$SERVICE_PATH/compose.yml" ]]; then
    error "compose.yml not found in service directory: $SERVICE_PATH"
fi

# Create logs directory
mkdir -p "$LOG_DIR"

# Start deployment
SERVICE_NAME=$(basename "$SERVICE_PATH")
log "Starting deployment of service: $SERVICE_NAME"
log "Service path: $SERVICE_PATH"

# Pre-deployment checks
log "Performing pre-deployment checks..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    error "Docker is not running or not accessible"
fi

# Check if required networks exist
REQUIRED_NETWORKS=("traefik" "database" "internal")
for network in "${REQUIRED_NETWORKS[@]}"; do
    if ! docker network ls --format "{{.Name}}" | grep -q "^${network}$"; then
        warning "Network $network does not exist. It will be created."
    fi
done

# Validate compose file
log "Validating compose file..."
if ! docker compose -f "$SERVICE_PATH/compose.yml" config >/dev/null 2>&1; then
    error "Invalid compose file: $SERVICE_PATH/compose.yml"
fi

success "Pre-deployment checks completed"

# Exit if check-only mode
if [[ "$CHECK_ONLY" == true ]]; then
    log "Check-only mode enabled. Exiting."
    exit 0
fi

# Show what will be deployed
log "Deployment plan:"
if [[ "$VERBOSE" == true ]] || [[ "$DRY_RUN" == true ]]; then
    docker compose -f "$SERVICE_PATH/compose.yml" config
fi

# Exit if dry-run mode
if [[ "$DRY_RUN" == true ]]; then
    log "Dry-run mode enabled. Exiting."
    exit 0
fi

# Record start time
START_TIME=$(date +%s)

# Deploy the service
log "Deploying service: $SERVICE_NAME"

cd "$SERVICE_PATH"

# Pull images first
log "Pulling container images..."
if [[ "$VERBOSE" == true ]]; then
    docker compose pull
else
    docker compose pull >/dev/null 2>&1
fi

# Start the service
log "Starting service containers..."
if [[ "$VERBOSE" == true ]]; then
    docker compose up -d
else
    docker