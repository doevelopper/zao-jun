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
    docker compose up -d >/dev/null 2>&1
fi

# Wait for service to be healthy
log "Waiting for service to become healthy..."
TIMEOUT=300  # 5 minutes
INTERVAL=10
ELAPSED=0

while [[ $ELAPSED -lt $TIMEOUT ]]; do
    if docker compose ps --services --filter "status=running" | grep -q "$SERVICE_NAME"; then
        # Check if service has health check
        if docker compose ps --format "{{.Service}} {{.Status}}" | grep -q "healthy"; then
            success "Service is running and healthy"
            break
        elif docker compose ps --format "{{.Service}} {{.Status}}" | grep -q "unhealthy"; then
            error "Service is unhealthy. Check logs: docker compose logs $SERVICE_NAME"
        else
            log "Service is running, waiting for health check..."
        fi
    else
        log "Waiting for service to start..."
    fi
    
    sleep $INTERVAL
    ELAPSED=$((ELAPSED + INTERVAL))
done

if [[ $ELAPSED -ge $TIMEOUT ]]; then
    warning "Service deployment timeout reached. Service may still be starting."
fi

# Record end time and calculate duration
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

success "Service deployment completed in ${DURATION} seconds"

# Show service information
log "Service information:"
docker compose ps --format "table {{.Service}}\t{{.Status}}\t{{.Ports}}"

# Return to original directory
cd "$PLATFORM_ROOT"

log "Deployment of $SERVICE_NAME completed successfully"

---

# scripts/health-check.sh
#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
PLATFORM_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="${PLATFORM_ROOT}/logs"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Logging functions
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Help function
show_help() {
    cat << EOF
Platform Health Check Script

Usage: $0 [OPTIONS] [SERVICE_NAME]

Arguments:
    SERVICE_NAME    Specific service to check (optional, checks all if not specified)

Options:
    -h, --help      Show this help message
    -q, --quiet     Suppress non-essential output
    -j, --json      Output results in JSON format
    -w, --watch     Continuous monitoring mode

Examples:
    $0                      # Check all services
    $0 traefik             # Check specific service
    $0 --json              # JSON output
    $0 --watch             # Continuous monitoring

EOF
}

# Parse arguments
QUIET=false
JSON_OUTPUT=false
WATCH_MODE=false
SPECIFIC_SERVICE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -q|--quiet)
            QUIET=true
            shift
            ;;
        -j|--json)
            JSON_OUTPUT=true
            shift
            ;;
        -w|--watch)
            WATCH_MODE=true
            shift
            ;;
        *)
            if [[ -z "$SPECIFIC_SERVICE" ]]; then
                SPECIFIC_SERVICE="$1"
            else
                error "Unknown argument: $1"
                exit 1
            fi
            shift
            ;;
    esac
done

# Health check function
check_service_health() {
    local service_name="$1"
    local result=""
    
    if ! docker ps --format "{{.Names}}" | grep -q "^${service_name}$"; then
        result="not_running"
    else
        local health_status=$(docker inspect --format='{{.State.Health.Status}}' "$service_name" 2>/dev/null || echo "no_healthcheck")
        
        case "$health_status" in
            "healthy")
                result="healthy"
                ;;
            "unhealthy")
                result="unhealthy"
                ;;
            "starting")
                result="starting"
                ;;
            "no_healthcheck")
                # Check if container is running
                if docker ps --format "{{.Names}}" | grep -q "^${service_name}$"; then
                    result="running_no_healthcheck"
                else
                    result="not_running"
                fi
                ;;
            *)
                result="unknown"
                ;;
        esac
    fi
    
    echo "$result"
}

# Get all platform services
get_platform_services() {
    docker ps --filter "label=platform.service" --format "{{.Names}}" | sort
}

# Single health check
perform_health_check() {
    local services=()
    
    if [[ -n "$SPECIFIC_SERVICE" ]]; then
        services=("$SPECIFIC_SERVICE")
    else
        readarray -t services < <(get_platform_services)
    fi
    
    if [[ ${#services[@]} -eq 0 ]]; then
        if [[ "$JSON_OUTPUT" == true ]]; then
            echo '{"error": "No platform services found", "services": []}'
        else
            warning "No platform services found"
        fi
        return 1
    fi
    
    local results=()
    local healthy_count=0
    local total_count=${#services[@]}
    
    for service in "${services[@]}"; do
        local status=$(check_service_health "$service")
        local domain=$(docker inspect --format='{{index .Config.Labels "platform.domain"}}' "$service" 2>/dev/null || echo "unknown")
        local description=$(docker inspect --format='{{index .Config.Labels "platform.description"}}' "$service" 2>/dev/null || echo "")
        
        if [[ "$status" == "healthy" || "$status" == "running_no_healthcheck" ]]; then
            ((healthy_count++))
        fi
        
        if [[ "$JSON_OUTPUT" == true ]]; then
            results+=("{\"name\": \"$service\", \"status\": \"$status\", \"domain\": \"$domain\", \"description\": \"$description\"}")
        else
            local status_icon=""
            local status_color=""
            
            case "$status" in
                "healthy"|"running_no_healthcheck")
                    status_icon="✅"
                    status_color="$GREEN"
                    ;;
                "unhealthy"|"not_running")
                    status_icon="❌"
                    status_color="$RED"
                    ;;
                "starting")
                    status_icon="🔄"
                    status_color="$YELLOW"
                    ;;
                *)
                    status_icon="❓"
                    status_color="$YELLOW"
                    ;;
            esac
            
            if [[ "$QUIET" != true ]]; then
                printf "%-20s %s %s%-15s%s %s\n" "$service" "$status_icon" "$status_color" "$status" "$NC" "$description"
            fi
        fi
    done
    
    if [[ "$JSON_OUTPUT" == true ]]; then
        local services_json=$(IFS=,; echo "${results[*]}")
        echo "{\"timestamp\": \"$(date -Iseconds)\", \"total\": $total_count, \"healthy\": $healthy_count, \"services\": [$services_json]}"
    else
        if [[ "$QUIET" != true ]]; then
            echo ""
            success "Health check completed: $healthy_count/$total_count services healthy"
        fi
        
        if [[ $healthy_count -lt $total_count ]]; then
            return 1
        fi
    fi
}

# Continuous monitoring mode
watch_services() {
    if [[ "$JSON_OUTPUT" != true ]]; then
        log "Starting continuous health monitoring (Press Ctrl+C to stop)"
        echo ""
    fi
    
    while true; do
        if [[ "$JSON_OUTPUT" != true ]]; then
            clear
            echo -e "${BLUE}Platform Health Dashboard - $(date)${NC}"
            echo "=================================================="
            printf "%-20s %-2s %-15s %s\n" "SERVICE" "ST" "STATUS" "DESCRIPTION"
            echo "--------------------------------------------------"
        fi
        
        perform_health_check
        
        if [[ "$JSON_OUTPUT" != true ]]; then
            echo ""
            echo "Press Ctrl+C to stop monitoring..."
        fi
        
        sleep 30
    done
}

# Create logs directory
mkdir -p "$LOG_DIR"

# Main execution
if [[ "$WATCH_MODE" == true ]]; then
    watch_services
else
    perform_health_check
fi

---

# scripts/cleanup.sh
#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
PLATFORM_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="${PLATFORM_ROOT}/logs"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Logging functions
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "${LOG_DIR}/cleanup_${TIMESTAMP}.log"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "${LOG_DIR}/cleanup_${TIMESTAMP}.log"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "${LOG_DIR}/cleanup_${TIMESTAMP}.log"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "${LOG_DIR}/cleanup_${TIMESTAMP}.log"
}

# Help function
show_help() {
    cat << EOF
Platform Cleanup Script

Usage: $0 [OPTIONS] [SERVICE_NAME]

Arguments:
    SERVICE_NAME    Specific service to cleanup (optional)

Options:
    -h, --help      Show this help message
    -a, --all       Clean up everything (services, volumes, networks, images)
    -s, --services  Remove stopped services only
    -v, --volumes   Remove unused volumes
    -n, --networks  Remove unused networks  
    -i, --images    Remove unused images
    -l, --logs      Clean up old log files
    -d, --dry-run   Show what would be cleaned without executing
    -f, --force     Skip confirmation prompts

Examples:
    $0 nginx                    # Remove specific service
    $0 --services              # Remove stopped services
    $0 --all                   # Complete cleanup
    $0 --dry-run --all         # Show what would be cleaned

EOF
}

# Parse arguments
CLEANUP_ALL=false
CLEANUP_SERVICES=false
CLEANUP_VOLUMES=false
CLEANUP_NETWORKS=false
CLEANUP_IMAGES=false
CLEANUP_LOGS=false
DRY_RUN=false
FORCE=false
SPECIFIC_SERVICE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -a|--all)
            CLEANUP_ALL=true
            shift
            ;;
        -s|--services)
            CLEANUP_SERVICES=true
            shift
            ;;
        -v|--volumes)
            CLEANUP_VOLUMES=true
            shift
            ;;
        -n|--networks)
            CLEANUP_NETWORKS=true
            shift
            ;;
        -i|--images)
            CLEANUP_IMAGES=true
            shift
            ;;
        -l|--logs)
            CLEANUP_LOGS=true
            shift
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        *)
            if [[ -z "$SPECIFIC_SERVICE" ]]; then
                SPECIFIC_SERVICE="$1"
            else
                error "Unknown argument: $1"
                exit 1
            fi
            shift
            ;;
    esac
done

# Set defaults if no specific cleanup type specified
if [[ "$CLEANUP_ALL" == false && "$CLEANUP_SERVICES" == false && "$CLEANUP_VOLUMES" == false && 
      "$CLEANUP_NETWORKS" == false && "$CLEANUP_IMAGES" == false && "$CLEANUP_LOGS" == false && 
      -z "$SPECIFIC_SERVICE" ]]; then
    CLEANUP_SERVICES=true
fi

# If --all is specified, enable all cleanup types
if [[ "$CLEANUP_ALL" == true ]]; then
    CLEANUP_SERVICES=true
    CLEANUP_VOLUMES=true
    CLEANUP_NETWORKS=true
    CLEANUP_IMAGES=true
    CLEANUP_LOGS=true
fi

# Create logs directory
mkdir -p "$LOG_DIR"

# Confirmation function
confirm() {
    if [[ "$FORCE" == true || "$DRY_RUN" == true ]]; then
        return 0
    fi
    
    echo -e "${YELLOW}$1${NC}"
    read -p "Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "Operation cancelled by user"
        exit 0
    fi
}

# Execute or show command
execute_or_show() {
    local cmd="$1"
    local description="$2"
    
    if [[ "$DRY_RUN" == true ]]; then
        echo "[DRY-RUN] $description: $cmd"
    else
        log "$description"
        eval "$cmd"
    fi
}

log "Starting platform cleanup"

# Clean specific service
if [[ -n "$SPECIFIC_SERVICE" ]]; then
    log "Cleaning up specific service: $SPECIFIC_SERVICE"
    
    # Find service compose file
    SERVICE_PATH=""
    while IFS= read -r -d '' file; do
        if grep -q "$SPECIFIC_SERVICE" "$file" 2>/dev/null; then
            SERVICE_PATH=$(dirname "$file")
            break
        fi
    done < <(find "$PLATFORM_ROOT/domains" -name "compose.yml" -print0)
    
    if [[ -z "$SERVICE_PATH" ]]; then
        error "Service $SPECIFIC_SERVICE not found"
        exit 1
    fi
    
    confirm "This will stop and remove the service: $SPECIFIC_SERVICE"
    
    cd "$SERVICE_PATH"
    execute_or_show "docker compose down -v" "Stopping and removing $SPECIFIC_SERVICE"
    cd "$PLATFORM_ROOT"
    
    success "Service $SPECIFIC_SERVICE cleaned up"
    exit 0
fi

# Clean up stopped services
if [[ "$CLEANUP_SERVICES" == true ]]; then
    log "Identifying stopped services to clean up"
    
    STOPPED_SERVICES=$(docker ps -a --filter "status=exited" --filter "label=platform.service" --format "{{.Names}}" || echo "")
    
    if [[ -n "$STOPPED_SERVICES" && "$STOPPED_SERVICES" != "" ]]; then
        confirm "Remove stopped platform services: $STOPPED_SERVICES"
        execute_or_show "docker rm $STOPPED_SERVICES" "Removing stopped services"
    else
        log "No stopped platform services found"
    fi
fi

# Clean up unused volumes
if [[ "$CLEANUP_VOLUMES" == true ]]; then
    log "Identifying unused volumes"
    
    UNUSED_VOLUMES=$(docker volume ls -q --filter "dangling=true" | grep -E "(platform|traefik|postgres|redis|rabbitmq)" || echo "")
    
    if [[ -n "$UNUSED_VOLUMES" && "$UNUSED_VOLUMES" != "" ]]; then
        confirm "Remove unused platform volumes: $UNUSED_VOLUMES"
        execute_or_show "docker volume rm $UNUSED_VOLUMES" "Removing unused volumes"
    else
        log "No unused platform volumes found"
    fi
fi

# Clean up unused networks
if [[ "$CLEANUP_NETWORKS" == true ]]; then
    log "Identifying unused networks"
    
    execute_or_show "docker network prune -f" "Removing unused networks"
fi

# Clean up unused images
if [[ "$CLEANUP_IMAGES" == true ]]; then
    log "Identifying unused images"
    
    confirm "Remove unused Docker images (this may take some time)"
    execute_or_show "docker image prune -a -f" "Removing unused images"
fi

# Clean up old log files
if [[ "$CLEANUP_LOGS" == true ]]; then
    log "Cleaning up old log files"
    
    # Remove log files older than 30 days
    OLD_LOGS=$(find "$LOG_DIR" -name "*.log" -mtime +30 2>/dev/null || echo "")
    
    if [[ -n "$OLD_LOGS" && "$OLD_LOGS" != "" ]]; then
        confirm "Remove log files older than 30 days"
        execute_or_show "find '$LOG_DIR' -name '*.log' -mtime +30 -delete" "Removing old log files"
    else
        log "No old log files found"
    fi
    
    # Compress recent log files
    RECENT_LOGS=$(find "$LOG_DIR" -name "*.log" -mtime +7 -mtime -30 2>/dev/null || echo "")
    
    if [[ -n "$RECENT_LOGS" && "$RECENT_LOGS" != "" ]]; then
        execute_or_show "find '$LOG_DIR' -name '*.log' -mtime +7 -mtime -30 -exec gzip {} \;" "Compressing recent log files"
    fi
fi

# Show cleanup summary
if [[ "$DRY_RUN" != true ]]; then
    log "Cleanup summary:"
    echo "Docker system df:"
    docker system df
    echo ""
    success "Platform cleanup completed"
else
    log "Dry-run completed. Use --force to execute the cleanup"
fi

---

# docs/onboarding.md
# Service Onboarding Guide

This guide explains how to onboard new services to the Modular Container Platform.

## Quick Start (< 10 minutes)

### Prerequisites

- Docker and Docker Compose installed
- Access to the platform repository
- Basic understanding of containerized applications

### Step 1: Choose a Template

Navigate to the `templates/` directory and choose the appropriate template:

- `basic-service/` - For simple web applications
- `database-service/` - For database services  
- `web-service/` - For complex web applications with multiple components

### Step 2: Create Service Directory

```bash
# Choose appropriate domain
mkdir -p domains/[DOMAIN]/[SERVICE-NAME]/
cp -r templates/basic-service/* domains/[DOMAIN]/[SERVICE-NAME]/
```

Available domains:
- `core/` - Essential platform services
- `data/` - Database and storage services
- `monitoring/` - Observability and metrics
- `automation/` - Workflow and CI/CD tools
- `ai-ml/` - AI and machine learning services
- `development/` - Development tools and environments
- `utilities/` - General utility services
- `communication/` - Messaging and collaboration tools

### Step 3: Configure Your Service

Edit the `compose.yml` file and replace template variables:

```yaml
services:
  myservice:  # Replace with your service name
    image: myorg/myapp:latest  # Your container image
    container_name: myservice
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql://user:pass@postgresql:5432/mydb
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.myservice.rule=Host(`myservice.localhost`)"
      - "traefik.http.routers.myservice.entrypoints=websecure"
      - "traefik.http.routers.myservice.tls.certresolver=letsencrypt"
      - "traefik.http.services.myservice.loadbalancer.server.port=8080"
      - "platform.domain=applications"
      - "platform.service=myservice"
      - "platform.description=My awesome service"
```

### Step 4: Deploy Your Service

```bash
./scripts/deploy.sh ./domains/[DOMAIN]/[SERVICE-NAME]/
```

The script will:
1. Validate your configuration
2. Pull required container images
3. Start your service
4. Verify health checks
5. Register with Traefik for routing

### Step 5: Verify Deployment

- Check service status: `./scripts/health-check.sh myservice`
- Access via browser: `https://myservice.localhost`
- View in platform dashboard: `https://platform.localhost`

## Advanced Configuration

### Custom Health Checks

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s
```

### Environment-Specific Configuration

Create environment files:

```bash
# .env.production
DATABASE_URL=postgresql://prod-user:prod-pass@prod-db:5432/mydb
REDIS_URL=redis://prod-redis:6379

# .env.development  
DATABASE_URL=postgresql://dev-user:dev-pass@postgresql:5432/mydb_dev
REDIS_URL=redis://redis:6379
```

### Database Integration

For services requiring database access:

```yaml
services:
  myservice:
    # ... other config
    depends_on:
      - postgresql
    networks:
      - traefik
      - database
    environment:
      - DATABASE_URL=postgresql://myservice:myservice_password@postgresql:5432/myservice

networks:
  traefik:
    external: true
  database:
    external: true
```

### SSL/TLS Configuration

The platform automatically provides SSL certificates via Let's Encrypt. For custom certificates:

```yaml
labels:
  - "traefik.http.routers.myservice.tls=true"
  - "traefik.http.routers.myservice.tls.certresolver=letsencrypt"
  # OR for custom certs:
  - "traefik.http.routers.myservice.tls.domains[0].main=myservice.example.com"
```

### Resource Limits

```yaml
services:
  myservice:
    # ... other config
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## Troubleshooting

### Service Won't Start

1. Check logs: `docker compose -f domains/[DOMAIN]/[SERVICE]/compose.yml logs`
2. Verify configuration: `./scripts/deploy.sh --check domains/[DOMAIN]/[SERVICE]/`
3. Test connectivity: `docker exec -it [SERVICE] /bin/sh`

### Routing Issues

1. Verify Traefik labels are correct
2. Check Traefik dashboard: `https://traefik.localhost`
3. Ensure service is on the `traefik` network
4. Verify domain name resolution

### Health Check Failures

1. Test health endpoint manually: `curl http://localhost:[PORT]/health`
2. Adjust health check parameters (timeout, interval, retries)
3. Verify the health check command exists in the container

### Performance Issues

1. Check resource usage: `docker stats [SERVICE]`
2. Review logs for errors or warnings
3. Monitor database connections and queries
4. Consider scaling horizontally

## Best Practices

### Naming Conventions

- Use kebab-case for service names: `my-service`
- Include version in image tags: `myorg/myapp:v1.2.3`
- Use descriptive container names

### Security

- Never expose database ports directly
- Use environment variables for secrets
- Implement proper health checks
- Keep container images updated via Watchtower

### Monitoring

- Include platform labels for service discovery
- Implement structured logging
- Expose metrics endpoints when possible
- Use meaningful health check endpoints

### Documentation

- Document environment variables
- Include deployment notes
- Specify resource requirements
- Provide troubleshooting guides

## Service Templates

### Basic Web Service

```yaml
services:
  webapp:
    image: nginx:alpine
    container_name: webapp
    restart: unless-stopped
    volumes:
      - ./html:/usr/share/nginx/html:ro
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.webapp.rule=Host(`webapp.localhost`)"
      - "traefik.http.routers.webapp.entrypoints=websecure"
      - "traefik.http.routers.webapp.tls.certresolver=letsencrypt"
      - "platform.domain=applications"
      - "platform.service=webapp"
    networks:
      - traefik
```

### Database Service

```yaml
services:
  mongodb:
    image: mongo:6
    container_name: mongodb
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: secure_password
    volumes:
      - mongodb_data:/data/db
    labels:
      - "platform.domain=data"
      - "platform.service=mongodb"
    networks:
      - database
    ports:
      - "127.0.0.1:27017:27017"

volumes:
  mongodb_data:
```

### API Service with Database

```yaml
services:
  api:
    image: myorg/myapi:latest
    container_name: myapi
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql://api:api_password@postgresql:5432/api
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET=your-jwt-secret
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`api.localhost`)"
      - "traefik.http.routers.api.entrypoints=websecure"
      - "traefik.http.routers.api.tls.certresolver=letsencrypt"
      - "platform.domain=applications"
      - "platform.service=api"
    networks:
      - traefik
      - database
    depends_on:
      - postgresql
      - redis
```

## Support

- Platform documentation: `/docs/`
- Health monitoring: `https://healthchecks.localhost`
- Traefik dashboard: `https://traefik.localhost`
- Platform homepage: `https://platform.localhost`

For issues or questions, check the troubleshooting guide or review the platform logs in the `logs/` directory.

---

# docs/troubleshooting.md
# Troubleshooting Guide

This guide helps diagnose and resolve common issues with the Modular Container Platform.

## Quick Diagnostics

### Platform Health Check

```bash
# Check all services
./scripts/health-check.sh

# Check specific service
./scripts/health-check.sh traefik

# Continuous monitoring
./scripts/health-check.sh --watch
```

### Common Issues Checklist

- [ ] Docker daemon is running
- [ ] Required networks exist (traefik, database, internal)
- [ ] Core services are healthy (nginx, traefik)
- [ ] DNS resolution works for *.localhost domains
- [ ] Ports 80 and 443 are available
- [ ] Sufficient disk space and memory

## Service Issues

### Service Won't Start

**Symptoms**: Container exits immediately or fails to start

**Diagnosis**:
```bash
# Check container logs
docker compose -f domains/[DOMAIN]/[SERVICE]/compose.yml logs

# Check container status
docker ps -a | grep [SERVICE]

# Inspect container configuration
docker inspect [SERVICE]
```

**Common Causes & Solutions**:

1. **Port Conflicts**
   ```bash
   # Check what's using the port
   netstat -tlnp | grep :80
   # Solution: Change port or stop conflicting service
   ```

2. **Missing Environment Variables**
   ```yaml
   # Add required environment variables
   environment:
     - REQUIRED_VAR=value
   ```

3. **Volume Mount Issues**
   ```bash
   # Check if paths exist and have correct permissions
   ls -la /host/path/
   # Fix permissions
   chmod 755 /host/path/
   ```

4. **Network Issues**
   ```bash
   # Ensure networks exist
   docker network ls
   # Create if missing
   docker network create traefik
   ```

### Service Starts But Not Accessible

**Symptoms**: Container running but HTTP requests fail

**Diagnosis**:
```bash
# Check Traefik routes
curl -k https://traefik.localhost/api/http/routers

# Test service directly
docker exec -it [SERVICE] curl localhost:[PORT]/health

# Check Traefik logs
docker logs traefik
```

**Solutions**:

1. **Incorrect Traefik Labels**
   ```yaml
   labels:
     - "traefik.enable=true"
     - "traefik.http.routers.[SERVICE].rule=Host(`[SERVICE].localhost`)"
     - "traefik.http.services.[SERVICE].loadbalancer.server.port=[PORT]"
   ```

2. **Service Not on Traefik Network**
   ```yaml
   networks:
     - traefik
   ```

3. **Wrong Internal Port**
   ```bash
   # Check what port service is listening on
   docker exec -it [SERVICE] netstat -tlnp
   ```

### Service Unhealthy

**Symptoms**: Health check fails repeatedly

**Diagnosis**:
```bash
# Check health check command
docker inspect [SERVICE] | jq '.[0].Config.Healthcheck'

# Test health check manually
docker exec -it [SERVICE] [HEALTHCHECK_COMMAND]
```

**Solutions**:

1. **Adjust Health Check Timing**
   ```yaml
   healthcheck:
     test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
     interval: 30s
     timeout: 10s
     retries: 3
     start_period: 60s  # Allow more time for startup
   ```

2. **Fix Health Check Endpoint**
   ```bash
   # Verify endpoint exists and returns 200
   curl -f http://localhost:8080/health
   ```

## Network Issues

### DNS Resolution Problems

**Symptoms**: Can't access services via *.localhost domains

**Solutions**:

1. **Add to /etc/hosts** (Linux/Mac):
   ```bash
   echo "127.0.0.1 platform.localhost traefik.localhost" >> /etc/hosts
   ```

2. **Windows hosts file**:
   ```
   # C:\Windows\System32\drivers\etc\hosts
   127.0.0.1 platform.localhost
   127.0.0.1 traefik.localhost
   ```

3. **Configure DNS Server**:
   ```bash
   # Use system DNS or configure local DNS server
   systemd-resolve --set-dns=127.0.0.1
   ```

### SSL/TLS Certificate