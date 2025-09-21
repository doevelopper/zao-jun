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
