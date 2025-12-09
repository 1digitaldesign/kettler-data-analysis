# Production Deployment Checklist

## Pre-Deployment

### Infrastructure
- [ ] Docker and Docker Compose installed and configured
- [ ] Sufficient disk space (50GB+ recommended)
- [ ] Network connectivity verified
- [ ] Firewall rules configured
- [ ] SSL certificates obtained (if using HTTPS)

### Configuration
- [ ] Environment variables configured
- [ ] Resource limits set appropriately
- [ ] Health checks configured
- [ ] Logging configured
- [ ] Monitoring set up

### Security
- [ ] Secrets stored securely (not in git)
- [ ] Non-root users in containers
- [ ] Image vulnerabilities scanned
- [ ] Network security configured
- [ ] Access controls in place

### Data
- [ ] Backup strategy defined
- [ ] Data migration plan ready
- [ ] Volume mounts configured
- [ ] Persistent storage verified

## Deployment Steps

### 1. Build Images
```bash
docker-compose build
```

### 2. Test Locally
```bash
docker-compose up -d
python3 scripts/monitoring/health_check.py
```

### 3. Create Backup
```bash
./scripts/deployment/backup.sh
```

### 4. Deploy
```bash
./scripts/deployment/deploy.sh production
```

### 5. Verify Deployment
```bash
# Check service status
docker-compose ps

# Check health
python3 scripts/monitoring/health_check.py

# Check logs
docker-compose logs --tail=50
```

## Post-Deployment

### Monitoring
- [ ] Services responding to health checks
- [ ] Resource usage within limits
- [ ] No error logs
- [ ] API endpoints responding
- [ ] Data processing working

### Testing
- [ ] Vector API endpoints tested
- [ ] ETL pipeline tested
- [ ] R analysis tested (if applicable)
- [ ] Parallel execution tested
- [ ] Scaling tested

### Documentation
- [ ] Deployment documented
- [ ] Runbooks created
- [ ] Troubleshooting guide updated
- [ ] Team notified

## Rollback Plan

If issues occur:

1. **Stop services**:
   ```bash
   docker-compose down
   ```

2. **Restore backup**:
   ```bash
   ./scripts/deployment/restore.sh backups/data_TIMESTAMP.tar.gz
   ```

3. **Redeploy previous version**:
   ```bash
   git checkout <previous-version>
   docker-compose up -d
   ```

## Maintenance

### Regular Tasks
- [ ] Monitor resource usage weekly
- [ ] Review logs weekly
- [ ] Update dependencies monthly
- [ ] Test backups monthly
- [ ] Security audit quarterly

### Scaling
- Monitor load and scale as needed
- Use auto-scaling if available
- Document scaling procedures

## Emergency Contacts

- **On-Call Engineer**: [Contact Info]
- **DevOps Team**: [Contact Info]
- **Database Admin**: [Contact Info]

## Useful Commands

```bash
# Health check
python3 scripts/monitoring/health_check.py

# Service status
docker-compose ps

# View logs
docker-compose logs -f service-name

# Scale services
docker-compose up -d --scale python-etl=5

# Backup
./scripts/deployment/backup.sh

# Restore
./scripts/deployment/restore.sh backups/file.tar.gz
```
