#!/bin/bash
# FlaskWatchdog Dependency Migration Script
# Usage: ./migrate_dependencies.sh [phase]
# Phases: backup, phase1, phase2, rollback

set -e

PHASE=${1:-help}
BACKUP_DIR="backups/dependencies"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

create_backup() {
    log_info "Creating backup..."
    mkdir -p "$BACKUP_DIR"

    if [ -f requirements.txt ]; then
        cp requirements.txt "$BACKUP_DIR/requirements_${TIMESTAMP}.txt"
        log_success "Backed up requirements.txt to $BACKUP_DIR/requirements_${TIMESTAMP}.txt"
    fi

    # Backup current installed packages
    pip freeze > "$BACKUP_DIR/pip_freeze_${TIMESTAMP}.txt"
    log_success "Saved current pip freeze to $BACKUP_DIR/pip_freeze_${TIMESTAMP}.txt"
}

phase1_security_patches() {
    log_info "Starting Phase 1: Security Patches & Backward Compatible Updates"

    create_backup

    log_info "Creating new requirements structure..."
    cp requirements-prod-recommended.txt requirements-prod.txt
    cp requirements-dev-recommended.txt requirements-dev.txt

    log_info "Installing production dependencies..."
    pip install -r requirements-prod.txt

    log_success "Phase 1 installation complete!"

    log_warning "Next steps:"
    echo "  1. Run tests: pytest --cov=app tests/"
    echo "  2. Test manually in browser"
    echo "  3. If tests pass, commit changes:"
    echo "     git add requirements-prod.txt requirements-dev.txt"
    echo "     git commit -m 'security: Phase 1 dependency updates'"
}

phase2_services() {
    log_info "Starting Phase 2: Backend Service Updates"

    create_backup

    log_warning "Phase 2 updates redis (3.x -> 5.x) and gunicorn (20.x -> 23.x)"
    log_warning "This may require configuration changes!"

    read -p "Continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_error "Aborted by user"
        exit 1
    fi

    log_info "Installing updated dependencies..."
    pip install -r requirements-prod.txt

    log_success "Phase 2 installation complete!"

    log_warning "Test checklist:"
    echo "  [ ] Celery worker starts: celery -A run.celery worker --loglevel=INFO"
    echo "  [ ] Celery beat starts: celery -A run.celery beat --loglevel=INFO"
    echo "  [ ] Redis connection works: redis-cli ping"
    echo "  [ ] Rate limiting works (test endpoints)"
    echo "  [ ] Background tasks execute"
    echo "  [ ] Run full test suite: pytest tests/"
}

rollback() {
    log_warning "Rolling back to previous dependencies..."

    if [ ! -d "$BACKUP_DIR" ]; then
        log_error "No backup directory found at $BACKUP_DIR"
        exit 1
    fi

    LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/requirements_*.txt | head -1)

    if [ -z "$LATEST_BACKUP" ]; then
        log_error "No backup found in $BACKUP_DIR"
        exit 1
    fi

    log_info "Latest backup: $LATEST_BACKUP"
    read -p "Rollback to this version? (y/N) " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp "$LATEST_BACKUP" requirements.txt
        pip install -r requirements.txt
        log_success "Rolled back to $LATEST_BACKUP"
    else
        log_error "Rollback cancelled"
        exit 1
    fi
}

run_security_audit() {
    log_info "Running security audit..."

    if ! command -v pip-audit &> /dev/null; then
        log_info "Installing pip-audit..."
        pip install pip-audit
    fi

    pip-audit -r requirements-prod.txt || {
        log_warning "Security vulnerabilities found! See output above."
        return 1
    }

    log_success "No security vulnerabilities found!"
}

run_tests() {
    log_info "Running test suite..."

    if ! command -v pytest &> /dev/null; then
        log_error "pytest not found. Install dev dependencies:"
        echo "  pip install -r requirements-dev.txt"
        exit 1
    fi

    pytest --cov=app tests/ -v

    if [ $? -eq 0 ]; then
        log_success "All tests passed!"
    else
        log_error "Tests failed! Review output above."
        exit 1
    fi
}

show_help() {
    cat << EOF
FlaskWatchdog Dependency Migration Script

Usage: ./migrate_dependencies.sh [command]

Commands:
  backup          Create a backup of current dependencies
  phase1          Apply Phase 1: Security patches (low risk)
  phase2          Apply Phase 2: Service updates (medium risk)
  rollback        Rollback to previous backup
  audit           Run security audit on current dependencies
  test            Run test suite
  help            Show this help message

Migration Phases:
  Phase 1 (Recommended Now):
    - Security patches for critical vulnerabilities
    - Backward compatible updates
    - Low risk, high impact

  Phase 2 (After Phase 1):
    - Update redis, gunicorn, celery
    - May require configuration changes
    - Medium risk, medium impact

Examples:
  ./migrate_dependencies.sh backup
  ./migrate_dependencies.sh phase1
  ./migrate_dependencies.sh audit
  ./migrate_dependencies.sh test

EOF
}

case $PHASE in
    backup)
        create_backup
        ;;
    phase1)
        phase1_security_patches
        ;;
    phase2)
        phase2_services
        ;;
    rollback)
        rollback
        ;;
    audit)
        run_security_audit
        ;;
    test)
        run_tests
        ;;
    help)
        show_help
        ;;
    *)
        log_error "Unknown command: $PHASE"
        echo
        show_help
        exit 1
        ;;
esac
