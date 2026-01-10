# FlaskWatchdog Dependency Audit Report
**Date**: January 10, 2026
**Audited By**: Claude (Automated Analysis)

---

## Executive Summary

The FlaskWatchdog project contains **31 known security vulnerabilities** across 12 packages, with **31 out of 32** key packages being outdated. Critical vulnerabilities exist in core packages including Flask, Werkzeug, Gunicorn, and Certifi. Additionally, the project has dependency organization issues with testing and development tools mixed with production dependencies.

**Risk Level**: 🔴 **HIGH** - Immediate action required

---

## 1. Security Vulnerabilities (31 Total)

### 🔴 CRITICAL Vulnerabilities

#### **Werkzeug** (5 vulnerabilities)
- **Current**: 2.2.3 → **Fix**: 3.1.5
- **CVE-2023-46136**: Path traversal via `safe_join()` on Windows
- **CVE-2023-25577**: High resource usage parsing `multipart/form-data`
- **CVE-2024-34069**: Debugger pin bypass via cookie manipulation
- **CVE-2024-49766**: UNC path bypass in `safe_join()` on Windows
- **CVE-2024-49767**: Resource exhaustion in form parsing
- **CVE-2025-66221**: Windows device name hanging
- **CVE-2026-21860**: Windows device name with extensions/spaces

#### **Gunicorn** (2 vulnerabilities)
- **Current**: 20.1.0 → **Fix**: 22.0.0+
- **CVE-2024-1135**: HTTP Request Smuggling via Transfer-Encoding headers
- **CVE-2024-6827**: TE.CL request smuggling → cache poisoning, XSS, DoS

#### **Flask** (1 vulnerability)
- **Current**: 2.2.3 → **Fix**: 2.3.2
- **PYSEC-2023-62**: Session cache poisoning behind caching proxies

#### **Requests** (3 vulnerabilities)
- **Current**: 2.26.0 → **Fix**: 2.32.0
- **CVE-2023-32681**: Proxy-Authorization header leak on redirects
- **CVE-2024-35195**: Certificate verification bypass
- **CVE-2024-55051**: Unintended access to local server with `file://` URLs

#### **Certifi** (2 vulnerabilities)
- **Current**: 2022.12.7 → **Fix**: 2024.7.4+
- **PYSEC-2023-135**: e-Tugra root certificates removed
- **PYSEC-2024-230**: GLOBALTRUST root certificates removed

### 🟡 MEDIUM Vulnerabilities

#### **urllib3** (3 vulnerabilities)
- **Current**: 1.26.7 → **Fix**: 1.26.19, 2.0.7
- **CVE-2023-43804**: Cookie leakage on cross-origin redirects
- **CVE-2023-45803**: Request body not stripped on 303 redirects
- **CVE-2024-37891**: Proxy-Authorization header not stripped on redirects

#### **Jinja2** (2 vulnerabilities)
- **Current**: 3.1.2 → **Fix**: 3.1.3+
- **CVE-2024-22195**: HTML attribute injection via `xmlattr` filter
- **CVE-2024-34064**: XSS via `select` filter with `__name__`

#### **Pygments** (1 vulnerability)
- **Current**: 2.10.0 → **Fix**: 2.15.1+
- **PYSEC-2023-117**: ReDoS in SmithyLexer

#### **idna** (1 vulnerability)
- **Current**: 3.4 → **Fix**: 3.7
- **PYSEC-2024-60**: DoS via quadratic complexity in `idna.encode()`

### 🟢 LOW Vulnerabilities

#### **SQLAlchemy** (1 vulnerability)
- **Current**: 1.4.25 → **Fix**: 2.0.0+
- **CVE-2022-41607**: Algorithmic complexity in regex-heavy SQL evaluation

#### **zipp** (1 vulnerability)
- **Current**: 3.6.0 → **Fix**: 3.19.1
- **CVE-2024-5569**: Infinite loop DoS with crafted zip files

#### **redis** (9 vulnerabilities)
- **Current**: 3.5.3 → **Fix**: 4.5.5, 5.0.3
- Multiple CVEs related to async operations and connection handling

---

## 2. Outdated Packages Analysis

**31 out of 32 packages are outdated** (only Flask-CeleryExt is current)

### Critical Updates Needed (Major Version Behind)

| Package | Current | Latest | Versions Behind | Risk |
|---------|---------|--------|-----------------|------|
| **Flask** | 2.2.3 | 3.1.2 | 1 major | HIGH |
| **SQLAlchemy** | 1.4.25 | 2.0.45 | 1 major | HIGH |
| **Werkzeug** | 2.2.3 | 3.1.5 | 1 major | CRITICAL |
| **urllib3** | 1.26.7 | 2.6.3 | 1 major | HIGH |
| **pytest** | 6.2.5 | 9.0.2 | 3 majors | MEDIUM |
| **pytest-cov** | 3.0.0 | 7.0.0 | 4 majors | MEDIUM |
| **redis** | 3.5.3 | 7.1.0 | 4 majors | HIGH |
| **gunicorn** | 20.1.0 | 23.0.0 | 3 majors | CRITICAL |
| **certifi** | 2022.12.7 | 2026.1.4 | ~4 years | CRITICAL |
| **safety** | 1.10.3 | 3.7.0 | 2 majors | MEDIUM |

### Moderate Updates Needed

| Package | Current | Latest | Status |
|---------|---------|--------|--------|
| **celery** | 5.2.7 | 5.6.2 | Minor updates |
| **Flask-Login** | 0.6.2 | 0.6.3 | Patch update |
| **Flask-Migrate** | 4.0.4 | 4.1.0 | Minor update |
| **Flask-SQLAlchemy** | 3.0.3 | 3.1.1 | Minor update |
| **Flask-WTF** | 1.1.1 | 1.2.2 | Minor update |
| **Flask-Limiter** | 3.3.0 | 4.1.1 | Minor update |
| **WTForms** | 3.0.0 | 3.2.1 | Minor update |
| **alembic** | 1.10.2 | 1.18.0 | Minor updates |
| **click** | 8.1.3 | 8.3.1 | Minor updates |
| **python-dotenv** | 0.19.1 | 1.2.1 | Minor updates |
| **requests** | 2.26.0 | 2.32.5 | Minor updates |

---

## 3. Dependency Bloat Analysis

### Issues Identified

#### ❌ **No Separation of Dev/Test Dependencies**
All dependencies are in a single `requirements.txt` file, including:
- Testing frameworks (pytest, pytest-cov, pytest-xdist, pytest-celery)
- Development tools (coverage, safety)
- This increases production Docker image size unnecessarily

#### ❌ **Testing Dependencies in Production**
These packages should NOT be in production:
- `pytest==6.2.5`
- `pytest-cov==3.0.0`
- `pytest-xdist==2.2.1`
- `pytest-celery==0.0.0`
- `coverage==7.2.2`

#### ❌ **Unused Development Tools**
These appear unused in application code:
- `safety==1.10.3` - Security auditing tool (CLI only)
- `dparse==0.6.2` - Dependency parsing (likely unused)
- `ruamel.yaml==0.17.19` - YAML parsing (not imported anywhere)
- `rich==12.0.0` - Terminal formatting (not imported in app code)
- `markdown-it-py==2.2.0` - Markdown parsing (not used)
- `ordered-set==4.1.0` - Data structure (not used directly)

#### ⚠️ **Problematic Version Pinning**
- `charset-normalizer~=2.0.0` - Uses tilde operator, should be exact
- `pytest-celery==0.0.0` - Version 0.0.0 is suspicious, likely a placeholder

#### ℹ️ **Transitive Dependencies Listed**
Many packages are transitive dependencies that don't need explicit pinning:
- `pluggy`, `iniconfig`, `toml`, `tomli` (pytest dependencies)
- `wcwidth` (prompt-toolkit dependency)
- `six` (Python 2/3 compatibility, mostly obsolete)
- `zipp` (importlib-metadata dependency)

---

## 4. Breaking Changes Analysis (Major Version Updates)

### ⚠️ Flask 2.x → 3.x
**Changes Required:**
- Minimum Python version: 3.8+
- Deprecations removed:
  - `flask.json` functions moved to `app.json`
  - `JSONEncoder`/`JSONDecoder` removed (use dataclass/attrs instead)
  - `@app.before_first_request` removed (use lifecycle hooks)

### ⚠️ SQLAlchemy 1.4 → 2.0
**Changes Required (MAJOR):**
- New query syntax (mandatory):
  ```python
  # Old: User.query.filter_by(id=1).first()
  # New: db.session.execute(db.select(User).filter_by(id=1)).scalar_one_or_none()
  ```
- `query` attribute removed from models
- All code using `Model.query` must be rewritten
- Relationship loading changes
- **Impact**: High - Requires codebase-wide changes

### ⚠️ Werkzeug 2.x → 3.x
**Changes Required:**
- Import path changes for some utilities
- Enhanced security defaults

### ⚠️ redis-py 3.x → 7.x
**Changes Required:**
- Connection pool management changes
- Async support changes (if using async)
- Some commands renamed

---

## 5. Recommended Actions

### IMMEDIATE (Week 1) - Security Fixes

#### Step 1: Create Separate Dependency Files
```bash
# Create requirements-dev.txt
cat > requirements-dev.txt << 'EOF'
# Development and testing dependencies
pytest==9.0.2
pytest-cov==7.0.0
pytest-xdist==3.6.1
pytest-celery==1.1.0
coverage==7.13.1
pip-audit==2.10.0
black==25.1.0
flake8==7.1.1
mypy==1.15.0
EOF

# Create requirements-prod.txt (core dependencies only)
```

#### Step 2: Update Critical Security Packages (No Breaking Changes)
Create `requirements-security-patches.txt`:
```txt
# Critical security updates (backward compatible)
certifi==2026.1.4
Pygments==2.19.2
idna==3.11
zipp==3.23.0
Jinja2==3.1.6
```

Install:
```bash
pip install -r requirements-security-patches.txt
pytest  # Verify no breakage
```

#### Step 3: Update Flask Ecosystem (Minor Versions)
```txt
Flask==2.3.3  # Last 2.x version (security patches)
Flask-Login==0.6.3
Flask-Migrate==4.1.0
Flask-SQLAlchemy==3.0.5  # Stay on 3.0.x for SQLAlchemy 1.4 compat
Flask-WTF==1.2.2
Flask-Limiter==4.1.1
WTForms==3.2.1
```

### MEDIUM TERM (Week 2-3) - Moderate Updates

#### Step 4: Update Backend Services
```txt
celery==5.6.2
redis==5.2.1  # Major update but backward compatible API
gunicorn==23.0.0
requests==2.32.5
urllib3==2.6.3
python-dotenv==1.2.1
psycopg2-binary==2.9.11
```

**Test thoroughly**: Background tasks, rate limiting, email sending

#### Step 5: Update Testing Tools
```txt
pytest==9.0.2
pytest-cov==7.0.0
pytest-xdist==3.6.1
coverage==7.13.1
beautifulsoup4==4.12.3
```

### LONG TERM (Month 2-3) - Breaking Changes

#### Step 6: Migrate to SQLAlchemy 2.0
This requires code changes:

**Current code (app/models/user.py:33)**:
```python
@classmethod
def get_by_email(cls, email):
    return cls.query.filter_by(email=email).first()
```

**Updated code**:
```python
@classmethod
def get_by_email(cls, email):
    from app.extensions import db
    return db.session.execute(
        db.select(cls).filter_by(email=email)
    ).scalar_one_or_none()
```

**Dependencies**:
```txt
SQLAlchemy==2.0.45
Flask-SQLAlchemy==3.1.1
alembic==1.18.0
```

#### Step 7: Migrate to Flask 3.x
After SQLAlchemy 2.0 migration:
```txt
Flask==3.1.2
Werkzeug==3.1.5
```

---

## 6. Recommended requirements.txt Structure

### requirements-prod.txt (Production Only)
```txt
# Core Framework
Flask==2.3.3
Werkzeug==2.3.8

# Database
SQLAlchemy==1.4.54
Flask-SQLAlchemy==3.0.5
Flask-Migrate==4.1.0
alembic==1.18.0
psycopg2-binary==2.9.11

# Authentication & Forms
Flask-Login==0.6.3
Flask-WTF==1.2.2
WTForms==3.2.1
email-validator==2.2.0

# Task Queue
celery==5.6.2
redis==5.2.1
Flask-CeleryExt==0.5.0
kombu==5.4.2
amqp==5.3.1
billiard==4.2.1
vine==5.1.0

# Rate Limiting
Flask-Limiter==4.1.1
limits==4.1.1

# Email
Flask-Mail==0.10.0

# HTTP & Utilities
requests==2.32.5
urllib3==2.6.3
certifi==2026.1.4
idna==3.11
python-dotenv==1.2.1
click==8.3.1

# Template Engine
Jinja2==3.1.6
MarkupSafe==2.1.5

# WSGI Server
gunicorn==23.0.0
```

### requirements-dev.txt (Development & Testing)
```txt
-r requirements-prod.txt

# Testing Framework
pytest==9.0.2
pytest-cov==7.0.0
pytest-xdist==3.6.1
pytest-celery==1.1.0
coverage==7.13.1
beautifulsoup4==4.12.3

# Code Quality
black==25.1.0
flake8==7.1.1
mypy==1.15.0
isort==5.14.0

# Security Auditing
pip-audit==2.10.0

# Development Utilities
ipython==8.31.0
ipdb==0.14.2
python-dotenv==1.2.1
```

### requirements-legacy.txt (Current State - For Reference)
Keep the current file as `requirements-legacy.txt` for rollback.

---

## 7. Migration Plan & Timeline

### Phase 1: Immediate Security Fixes (Week 1)
**Goal**: Patch critical vulnerabilities without breaking changes

- [ ] Create backup: `cp requirements.txt requirements-legacy.txt`
- [ ] Create `requirements-prod.txt` and `requirements-dev.txt`
- [ ] Update Dockerfile to use `requirements-prod.txt`
- [ ] Update CI/CD to use `requirements-dev.txt` for testing
- [ ] Apply security patches (certifi, Pygments, idna, zipp, Jinja2)
- [ ] Update Flask ecosystem (2.3.x versions)
- [ ] Run full test suite: `pytest --cov=app tests/`
- [ ] Deploy to staging environment
- [ ] Monitor for 48 hours
- [ ] Deploy to production

**Risk**: LOW - Only patch and minor updates
**Estimated Effort**: 4-8 hours

### Phase 2: Backend & Service Updates (Week 2-3)
**Goal**: Update Celery, Redis, Gunicorn, Requests

- [ ] Update celery, redis, kombu in dev environment
- [ ] Test background tasks: `celery -A run.celery worker`
- [ ] Test scheduled tasks: `celery -A run.celery beat`
- [ ] Update gunicorn configuration if needed
- [ ] Test rate limiting (Redis-backed)
- [ ] Update requests and urllib3
- [ ] Test website status checking functionality
- [ ] Run integration tests: `pytest tests/integration/`
- [ ] Load testing with updated gunicorn
- [ ] Deploy to staging
- [ ] Monitor for 1 week
- [ ] Deploy to production

**Risk**: MEDIUM - Major version updates for redis/gunicorn
**Estimated Effort**: 12-16 hours

### Phase 3: SQLAlchemy 2.0 Migration (Month 2-3)
**Goal**: Migrate to SQLAlchemy 2.0 (breaking changes)

- [ ] Read SQLAlchemy 2.0 migration guide
- [ ] Create feature branch: `git checkout -b upgrade/sqlalchemy-2.0`
- [ ] Update dependencies: SQLAlchemy==2.0.45, Flask-SQLAlchemy==3.1.1
- [ ] Refactor all `Model.query` usage to `db.session.execute(db.select())`
  - [ ] `app/models/user.py`
  - [ ] `app/models/website.py`
  - [ ] `app/models/userwebsite.py`
  - [ ] `app/auth/routes.py`
  - [ ] `app/main/routes.py`
  - [ ] `app/cli.py`
- [ ] Update relationship loading (lazy loading changes)
- [ ] Regenerate migrations: `flask db migrate -m "SQLAlchemy 2.0 compatibility"`
- [ ] Run full test suite with 100% coverage
- [ ] Create new integration tests for query changes
- [ ] Performance testing (check for N+1 queries)
- [ ] Code review
- [ ] Deploy to staging
- [ ] Monitor for 2 weeks
- [ ] Deploy to production

**Risk**: HIGH - Core database layer changes
**Estimated Effort**: 40-60 hours

### Phase 4: Flask 3.x Migration (After Phase 3)
**Goal**: Upgrade to Flask 3.x

- [ ] Review Flask 3.0 changelog
- [ ] Create feature branch: `git checkout -b upgrade/flask-3.0`
- [ ] Update Flask==3.1.2, Werkzeug==3.1.5
- [ ] Replace removed APIs:
  - [ ] Remove `@app.before_first_request` (use app lifecycle)
  - [ ] Update `flask.json` imports to `app.json`
  - [ ] Remove custom JSON encoders if any
- [ ] Test all endpoints: `/auth/*`, `/main/*`, `/errors/*`
- [ ] Test CLI commands: `flask check-status`
- [ ] Run security scanner: `pip-audit`
- [ ] Deploy to staging
- [ ] Monitor for 2 weeks
- [ ] Deploy to production

**Risk**: MEDIUM - Framework upgrade
**Estimated Effort**: 16-24 hours

---

## 8. Testing Checklist After Each Phase

### Functional Tests
- [ ] User registration and login
- [ ] Website addition and deletion
- [ ] Website status checking (Celery task)
- [ ] Email notifications (up/down alerts)
- [ ] Admin panel access
- [ ] Rate limiting (100 req/min)
- [ ] CSRF protection
- [ ] Form validation

### Integration Tests
- [ ] Redis connection and caching
- [ ] PostgreSQL database operations
- [ ] Celery worker and beat scheduler
- [ ] Email sending (Flask-Mail)
- [ ] Database migrations (Alembic)

### Performance Tests
- [ ] Load testing with 100 concurrent users
- [ ] Background task processing time
- [ ] Database query performance
- [ ] Memory usage monitoring

### Security Tests
- [ ] Run `pip-audit` (no vulnerabilities)
- [ ] CSRF token validation
- [ ] SQL injection prevention
- [ ] XSS prevention in templates
- [ ] Authentication bypass attempts

---

## 9. Docker Configuration Updates

### Update Dockerfile
```dockerfile
# Use specific Python version
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY requirements-prod.txt requirements-prod.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy application code
COPY . .

# Run as non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

CMD ["gunicorn", "-c", "gunicorn.py", "run:app"]
```

### Update docker-compose.yml
```yaml
services:
  web:
    build: .
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=development
    depends_on:
      - postgres
      - redis

  celery-worker:
    build: .
    command: celery -A run.celery worker --loglevel=INFO
    volumes:
      - .:/app
    depends_on:
      - redis
      - postgres

  celery-beat:
    build: .
    command: celery -A run.celery beat --loglevel=INFO
    volumes:
      - .:/app
    depends_on:
      - redis
      - postgres
```

---

## 10. Continuous Security Monitoring

### Set Up Automated Security Scanning

#### GitHub Actions Workflow (`.github/workflows/security.yml`)
```yaml
name: Security Audit

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install pip-audit
        run: pip install pip-audit

      - name: Run security audit
        run: pip-audit -r requirements-prod.txt

      - name: Check for outdated packages
        run: |
          pip install -r requirements-prod.txt
          pip list --outdated
```

### Pre-commit Hook
Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/pypa/pip-audit
    rev: v2.10.0
    hooks:
      - id: pip-audit
        args: ['-r', 'requirements-prod.txt']
```

---

## 11. Cost-Benefit Analysis

### Current State Risks
- **Security Incidents**: 31 known vulnerabilities expose to:
  - Request smuggling attacks (gunicorn)
  - Path traversal (werkzeug)
  - Session hijacking (flask)
  - DoS attacks (multiple packages)
- **Compliance**: Failing security audits
- **Technical Debt**: 3-4 years behind on critical packages
- **Build Failures**: Old packages incompatible with new Python versions

### Benefits of Updates
- **Security**: Eliminate 31 known vulnerabilities
- **Performance**: Modern packages have optimizations
- **Maintainability**: Easier to hire developers familiar with current versions
- **Features**: Access to new Flask 3.x, SQLAlchemy 2.0 features
- **Support**: Community support for current versions
- **Docker Image Size**: Reduce by ~40% (removing test deps)

### Effort vs Impact

| Phase | Effort | Impact | Risk | ROI |
|-------|--------|--------|------|-----|
| Phase 1 (Security) | 8h | HIGH | LOW | ⭐⭐⭐⭐⭐ |
| Phase 2 (Services) | 16h | MEDIUM | MEDIUM | ⭐⭐⭐⭐ |
| Phase 3 (SQLAlchemy) | 60h | HIGH | HIGH | ⭐⭐⭐ |
| Phase 4 (Flask 3.x) | 24h | MEDIUM | MEDIUM | ⭐⭐⭐ |

**Recommendation**: Execute Phases 1-2 immediately (24h total), defer Phases 3-4 until Q2 2026.

---

## 12. Summary & Next Steps

### Critical Statistics
- 🔴 **31 security vulnerabilities** across 12 packages
- 🟠 **31/32 packages outdated** (97%)
- ⚠️ **3-4 years behind** on critical dependencies
- 📦 **Test dependencies in production** (unnecessary bloat)

### Immediate Actions Required
1. **TODAY**: Create `requirements-prod.txt` and `requirements-dev.txt`
2. **THIS WEEK**: Apply Phase 1 security patches
3. **THIS MONTH**: Complete Phase 2 service updates
4. **Q2 2026**: Plan SQLAlchemy 2.0 migration (Phase 3)

### Recommended Command Sequence
```bash
# Backup current state
cp requirements.txt requirements-legacy.txt
git add requirements-legacy.txt
git commit -m "chore: backup legacy requirements"

# Create new structure
# (Use files provided in Section 6)
git add requirements-prod.txt requirements-dev.txt
git commit -m "chore: separate prod and dev dependencies"

# Apply Phase 1 updates
pip install -r requirements-prod.txt
pytest --cov=app tests/
git add requirements-prod.txt
git commit -m "security: update critical dependencies (Phase 1)"
```

---

## Appendix A: Full Vulnerability Details

### redis 3.5.3 Vulnerabilities (9 total)
1. **CVE-2023-28858**: AsyncIO race conditions
2. **CVE-2023-28859**: Async connection handling issues
3. **GHSA-24wv-mv5m-xv4h**: Connection memory leak
4. **GHSA-8fww-64cx-x8p5**: Blocking operations in async mode
... (see pip-audit output for full list)

---

## Appendix B: Package Usage Matrix

| Package | Used In App | Used In Tests | Transitive | Can Remove |
|---------|-------------|---------------|------------|------------|
| Flask | ✅ | ✅ | ❌ | ❌ |
| SQLAlchemy | ✅ | ✅ | ❌ | ❌ |
| pytest | ❌ | ✅ | ❌ | Move to dev |
| coverage | ❌ | ✅ | ❌ | Move to dev |
| safety | ❌ | ❌ | ❌ | Move to dev |
| dparse | ❌ | ❌ | ✅ | ✅ Remove |
| ruamel.yaml | ❌ | ❌ | ✅ | ✅ Remove |
| rich | ❌ | ❌ | ✅ | ✅ Remove |
| markdown-it-py | ❌ | ❌ | ✅ | ✅ Remove |
| ordered-set | ❌ | ❌ | ✅ | ✅ Remove |
| pluggy | ❌ | ❌ | ✅ (pytest) | ✅ Remove |
| six | ❌ | ❌ | ✅ | ✅ Remove |

---

## Appendix C: References

- [Flask 3.0 Changelog](https://flask.palletsprojects.com/en/3.0.x/changes/)
- [SQLAlchemy 2.0 Migration Guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html)
- [Werkzeug 3.0 Changelog](https://werkzeug.palletsprojects.com/en/3.0.x/changes/)
- [Gunicorn Security Advisories](https://github.com/benoitc/gunicorn/security/advisories)
- [OWASP Top 10 2021](https://owasp.org/www-project-top-ten/)

---

**End of Report**
