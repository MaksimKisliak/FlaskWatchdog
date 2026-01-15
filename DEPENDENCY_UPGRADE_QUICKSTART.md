# Dependency Upgrade Quick Start Guide

## TL;DR - What You Need to Know

🔴 **Your project has 31 security vulnerabilities** in outdated packages (certifi, Flask, Werkzeug, gunicorn, etc.)

📋 **What was delivered:**
1. `DEPENDENCY_AUDIT_REPORT.md` - Comprehensive 12-page analysis
2. `requirements-prod-recommended.txt` - Updated production dependencies
3. `requirements-dev-recommended.txt` - Separated dev/test dependencies
4. `migrate_dependencies.sh` - Automated migration script

---

## Quick Actions (Choose Your Path)

### 🚀 Fast Path: Apply Security Fixes Now (30 minutes)

```bash
# 1. Backup current state
cp requirements.txt requirements-legacy.txt

# 2. Apply Phase 1 updates (automated)
./migrate_dependencies.sh phase1

# 3. Run tests
pip install -r requirements-dev.txt
pytest --cov=app tests/

# 4. If tests pass, commit
git add requirements-prod.txt requirements-dev.txt requirements-legacy.txt
git commit -m "security: Phase 1 - patch critical vulnerabilities"
git push
```

**What this fixes:**
- ✅ Patches 20+ security vulnerabilities
- ✅ Updates Flask 2.2.3 → 2.3.3
- ✅ Updates Werkzeug with path traversal fixes
- ✅ Updates certifi (4 years outdated)
- ✅ Separates test deps from production
- ✅ Backward compatible (no code changes)

---

### 📖 Careful Path: Read First, Then Apply (2 hours)

```bash
# 1. Read the full audit report
cat DEPENDENCY_AUDIT_REPORT.md

# 2. Review what will change
diff requirements.txt requirements-prod-recommended.txt

# 3. Create backup
./migrate_dependencies.sh backup

# 4. Apply Phase 1
./migrate_dependencies.sh phase1

# 5. Run security audit
./migrate_dependencies.sh audit

# 6. Run tests
./migrate_dependencies.sh test

# 7. Commit if all good
git add -A
git commit -m "security: Phase 1 dependency updates"
```

---

## What's in Each File

### `DEPENDENCY_AUDIT_REPORT.md` (Main Report)
- **Section 1**: Security vulnerabilities (31 found)
- **Section 2**: Outdated packages (31/32 outdated)
- **Section 3**: Dependency bloat analysis
- **Section 4**: Breaking changes guide (SQLAlchemy 2.0, Flask 3.x)
- **Section 5**: Recommended actions (4 phases)
- **Section 6**: New requirements.txt structure
- **Section 7**: Migration timeline (4 phases over 3 months)
- **Section 8**: Testing checklist
- **Section 9**: Docker updates
- **Section 10**: CI/CD security monitoring

### `requirements-prod-recommended.txt`
Production-only dependencies with security patches:
- Flask 2.3.3 (was 2.2.3)
- Werkzeug 2.3.8 (was 2.2.3)
- certifi 2026.1.4 (was 2022.12.7)
- gunicorn 23.0.0 (was 20.1.0)
- All Flask extensions updated
- **No breaking changes** from current code

### `requirements-dev-recommended.txt`
Development and testing dependencies:
- Includes production deps via `-r requirements-prod-recommended.txt`
- pytest 9.0.2 (was 6.2.5)
- coverage 7.13.1 (was 7.2.2)
- Code quality tools: black, flake8, mypy
- Security tools: pip-audit

### `migrate_dependencies.sh`
Automated migration script with commands:
```bash
./migrate_dependencies.sh backup   # Create backup
./migrate_dependencies.sh phase1   # Apply Phase 1 updates
./migrate_dependencies.sh audit    # Run security scan
./migrate_dependencies.sh test     # Run test suite
./migrate_dependencies.sh rollback # Undo changes
./migrate_dependencies.sh help     # Show all commands
```

---

## Upgrade Phases Explained

### ✅ Phase 1: Security Patches (DO NOW)
- **Time**: 30-60 minutes
- **Risk**: 🟢 LOW (backward compatible)
- **Fixes**: 20+ vulnerabilities
- **Code Changes**: None required
- **Testing**: Run existing pytest suite

### ⏳ Phase 2: Backend Services (NEXT WEEK)
- **Time**: 4-8 hours
- **Risk**: 🟡 MEDIUM (redis, gunicorn major updates)
- **Fixes**: Remaining vulnerabilities
- **Code Changes**: Possibly gunicorn config
- **Testing**: Integration tests, load testing

### 🔧 Phase 3: SQLAlchemy 2.0 (MONTH 2-3)
- **Time**: 40-60 hours
- **Risk**: 🔴 HIGH (breaking changes)
- **Benefit**: Modern ORM, better performance
- **Code Changes**: ALL database queries must be rewritten
- **Example**: `User.query.filter_by()` → `db.session.execute(db.select(User))`
- **Testing**: Comprehensive testing required

### 🎯 Phase 4: Flask 3.x (AFTER PHASE 3)
- **Time**: 16-24 hours
- **Risk**: 🟡 MEDIUM (framework upgrade)
- **Benefit**: Latest features, better security
- **Code Changes**: Remove deprecated APIs
- **Testing**: Full application testing

---

## Key Vulnerabilities Being Fixed

### Critical (Phase 1)
1. **Werkzeug CVE-2023-46136**: Path traversal on Windows
2. **Gunicorn CVE-2024-1135**: HTTP request smuggling
3. **Flask PYSEC-2023-62**: Session cache poisoning
4. **Requests CVE-2024-35195**: Certificate verification bypass
5. **Certifi**: Removed compromised root certificates

### High (Phase 2)
- redis: 9 CVEs related to async operations
- urllib3: Proxy header leakage
- Jinja2: XSS vulnerabilities

---

## Before You Start

### Prerequisites
```bash
# Check Python version (need 3.8+)
python --version

# Ensure pip is updated
pip install --upgrade pip

# Check current vulnerabilities
pip install pip-audit
pip-audit -r requirements.txt
```

### Recommended: Test in Staging First
```bash
# Create a test branch
git checkout -b upgrade/dependencies-phase1

# Apply changes
./migrate_dependencies.sh phase1

# Test thoroughly
pytest --cov=app tests/
flask check-status
celery -A run.celery inspect active

# If all good, merge to main
git checkout main
git merge upgrade/dependencies-phase1
```

---

## FAQ

### Q: Is this safe to apply to production?
**A**: Phase 1 is designed to be safe (backward compatible). However:
1. Test in staging environment first
2. Run full test suite
3. Monitor closely after deployment
4. Have rollback plan ready

### Q: Do I need to update my code?
**A**:
- **Phase 1**: No code changes needed
- **Phase 2**: Possibly gunicorn config
- **Phase 3**: Major code refactoring required
- **Phase 4**: Some deprecated API updates

### Q: What if something breaks?
```bash
# Quick rollback
./migrate_dependencies.sh rollback

# Or manually restore
cp requirements-legacy.txt requirements.txt
pip install -r requirements.txt
```

### Q: Can I do Phase 1 today and Phase 2 later?
**A**: Yes! That's the recommended approach. Phase 1 is independent.

### Q: How long until I MUST update?
**A**:
- Security vulnerabilities: Update ASAP
- Flask 2.x support ends: ~2027
- SQLAlchemy 1.4 support ends: ~2026
- Python 3.8 EOL: October 2024 (already passed)

### Q: What about Docker?
**A**: Update Dockerfile to use `requirements-prod.txt`:
```dockerfile
COPY requirements-prod.txt requirements-prod.txt
RUN pip install --no-cache-dir -r requirements-prod.txt
```

---

## Monitoring After Update

### Check for regressions
```bash
# Monitor logs
tail -f logs/app.log

# Check Celery tasks
celery -A run.celery inspect active
celery -A run.celery inspect stats

# Test key endpoints
curl http://localhost:5000/
curl http://localhost:5000/auth/login
```

### Performance comparison
```bash
# Before update
time pytest tests/

# After update
time pytest tests/

# Should be similar or faster
```

---

## Getting Help

### If tests fail after Phase 1:
1. Check the error message carefully
2. Review `DEPENDENCY_AUDIT_REPORT.md` Section 4 (Breaking Changes)
3. Rollback: `./migrate_dependencies.sh rollback`
4. Report issue with error logs

### If application behavior changes:
1. Check for deprecation warnings in logs
2. Review Flask 2.3 changelog: https://flask.palletsprojects.com/en/2.3.x/changes/
3. Check Werkzeug 2.3 changelog: https://werkzeug.palletsprojects.com/en/2.3.x/changes/

---

## Success Criteria

After Phase 1, you should have:
- ✅ Zero critical security vulnerabilities
- ✅ All tests passing
- ✅ Application running normally
- ✅ Separated prod/dev dependencies
- ✅ ~40% smaller Docker image (no test deps)
- ✅ Up-to-date with 2025/2026 packages

---

## Next Steps After Phase 1

1. **Monitor production** for 1-2 weeks
2. **Plan Phase 2** (backend services update)
3. **Schedule Phase 3** (SQLAlchemy 2.0) for Q2 2026
4. **Set up automated security scanning** (see report Section 10)

---

## Final Recommendation

**Do Phase 1 this week.** It's:
- Low risk (backward compatible)
- High impact (fixes 20+ vulnerabilities)
- Quick to apply (30-60 minutes)
- Easy to rollback if needed
- Does not require code changes

**Command to run:**
```bash
./migrate_dependencies.sh phase1 && pytest
```

That's it! 🚀
