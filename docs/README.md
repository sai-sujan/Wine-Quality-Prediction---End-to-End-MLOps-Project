# Documentation

This folder contains all project documentation organized by category.

## 📁 Folder Structure

### `/aws` - AWS Deployment Documentation
Guides for deploying to AWS Lambda, ECR, S3, and API Gateway.

- **AWS_DEPLOYMENT_GUIDE.md** - Complete AWS deployment walkthrough
- **AWS_DEPLOYMENT_WORKFLOW.md** - Step-by-step deployment workflow
- **AWS_SETUP_GUIDE.md** - Initial AWS account and IAM setup
- **AWS_ECR_PERMISSIONS.md** - ECR permission requirements
- **fix_ecr_permissions.md** - ECR permission troubleshooting
- **LAMBDA_SIZE_FIX.md** - Lambda package size optimization history

### `/deployment` - Deployment Guides
General deployment documentation and guides.

- **DOCKER_DEPLOYMENT_GUIDE.md** - Docker-based Lambda deployment
- **QUICK_START.md** - Quick deployment guide
- **HYPERPARAMETER_CACHING.md** - Hyperparameter optimization caching
- **FASTAPI_GUIDE.md** - FastAPI local development guide

### `/troubleshooting` - CI/CD and Troubleshooting
GitHub Actions, CI/CD issues, and fixes.

- **CICD_SETUP.md** - GitHub Actions CI/CD configuration
- **GITHUB_ACTIONS_FIXES.md** - Common GitHub Actions issues and solutions

### `/archived` - Archived Documentation
Old documentation kept for reference but no longer actively maintained.

- **CLEANUP_SUMMARY.md** - Project cleanup history
- **PROJECT_STRUCTURE.md** - Old project structure documentation
- **QUICK_FIX_*.md** - Quick fix guides (superseded by current docs)
- **FIX_APPLIED.md** - Historical fix documentation
- **FASTAPI_BENEFITS.md** - FastAPI benefits (merged into FASTAPI_GUIDE.md)

---

## 🎯 Quick Links

### For First-Time Setup
1. Start with: [AWS Setup Guide](aws/AWS_SETUP_GUIDE.md)
2. Then: [Docker Deployment Guide](deployment/DOCKER_DEPLOYMENT_GUIDE.md)
3. Configure: [CI/CD Setup](troubleshooting/CICD_SETUP.md)

### For Deployment
1. Quick deploy: [Quick Start](deployment/QUICK_START.md)
2. Full workflow: [AWS Deployment Workflow](aws/AWS_DEPLOYMENT_WORKFLOW.md)
3. Docker method: [Docker Deployment](deployment/DOCKER_DEPLOYMENT_GUIDE.md)

### For Troubleshooting
1. GitHub Actions: [GitHub Actions Fixes](troubleshooting/GITHUB_ACTIONS_FIXES.md)
2. ECR Permissions: [ECR Permission Fix](aws/fix_ecr_permissions.md)
3. Lambda Size: [Lambda Size Fix](aws/LAMBDA_SIZE_FIX.md)

---

## 📝 Root Directory Docs

Important documentation kept in project root for visibility:

- **README.md** - Main project README (portfolio/demo)
- **API_TEST_RESULTS.md** - API performance and testing results
- **DOCKER_DEPLOYMENT_SUCCESS.md** - Current deployment solution summary

---

## 🔍 Finding Documentation

**By Topic**:
```bash
# AWS deployment
ls docs/aws/

# Docker and deployment
ls docs/deployment/

# CI/CD issues
ls docs/troubleshooting/

# Historical reference
ls docs/archived/
```

**Search all docs**:
```bash
grep -r "search term" docs/
```

---

## 📚 Documentation Standards

All documentation in this folder follows these standards:

1. **Markdown format** - Easy to read on GitHub
2. **Code examples** - Include working code snippets
3. **Step-by-step** - Clear sequential instructions
4. **Troubleshooting** - Common issues and solutions
5. **Up-to-date** - Reflects current implementation

---

## 🗂️ Document Lifecycle

- **Active**: Docs in `/aws`, `/deployment`, `/troubleshooting`
- **Archived**: Docs in `/archived` (kept for reference)
- **Root**: Portfolio/demo docs (README, API_TEST_RESULTS, DOCKER_DEPLOYMENT_SUCCESS)

When docs become outdated, they're moved to `/archived` rather than deleted.
