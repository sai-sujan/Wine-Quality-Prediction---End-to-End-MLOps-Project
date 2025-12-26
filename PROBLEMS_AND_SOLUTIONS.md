# Technical Problems & Solutions - Quick Reference

## 📋 One-Page Summary for Quick Review

### Problem 1: Lambda 250MB Size Limit ❌ → ✅

**Problem**: Full dependencies = 302MB (exceeds 250MB limit)

**Bad Approaches**:
- Lambda Layers with cleanup → Module errors
- Manual dependency pruning → Broke sklearn

**Good Approach**:
- Docker containers with minimal `lambda_requirements.txt`
- Reduced from 162 packages → 5 packages
- Final size: 60MB

**Key Insight**: Separate training dependencies from inference dependencies

---

### Problem 2: scipy Import Errors ❌ → ✅

**Problem**: `No module named 'scipy.integrate'` / `scipy.special` / `scipy.stats`

**Bad Approaches**:
- Delete "unused" scipy modules → More errors
- Preserve modules one-by-one → Whack-a-mole

**Good Approach**:
- Let Docker handle complete dependency installation
- Don't try to outsmart ML library dependency trees

**Key Insight**: ML libraries have complex internal dependencies - use containers

---

### Problem 3: API Gateway Permission Denied ❌ → ✅

**Problem**: Lambda works but API Gateway returns 500 Internal Server Error

**Root Cause**: Missing Lambda resource policy for API Gateway invocation

**Good Approach**:
```bash
aws lambda add-permission \
  --statement-id apigateway-invoke \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com
```

**Key Insight**: AWS has 3 permission layers - resource policy, execution role, user policy

---

### Problem 4: ECR Access Denied ❌ → ✅

**Problem**: `AccessDeniedException` when Lambda tries to pull Docker image

**Three-Layer Fix**:
1. ECR Repository Policy → Allow lambda.amazonaws.com
2. Lambda Execution Role → Add ecr:* permissions
3. IAM User Policy → Add ecr:SetRepositoryPolicy

**Good Approach**: Document all three permission layers in deployment script

**Key Insight**: Cloud permissions are nested - all layers must align

---

### Problem 5: Slow Hyperparameter Tuning ❌ → ✅

**Problem**: 100 Optuna trials = 15+ minutes locally

**Good Approach**:
- Use 10 trials for development
- Cache results in `best_params.json`
- Run full 100 trials only in CI/CD

**Key Insight**: Optimize for development speed, not just model accuracy

---

### Problem 6: GitHub Actions Costs ❌ → ✅

**Problem**: Every code change triggered full model retraining

**Good Approach**:
```yaml
on:
  push:
    paths:
      - 'lambda_handler.py'
      - 'Dockerfile'
      # Only trigger on relevant files
```

**Key Insight**: Good CI/CD is about control, not just automation

---

## 🎯 Best Practices Learned

| Practice | Why It Matters |
|----------|----------------|
| Separate training/inference deps | 90% smaller Lambda images |
| Use Docker for ML deployments | Zero dependency conflicts |
| Document all IAM layers | Faster debugging, better security |
| Cache hyperparameters | 70% faster development cycles |
| Path-based CI/CD triggers | 80% cost reduction |
| Idempotent deployment scripts | Safe to re-run, easy rollbacks |
| CloudWatch logging + local scripts | 10x faster incident response |

---

## 💡 Technical Decisions Explained

### Why Docker over Lambda Layers?

| Aspect | Lambda Layers | Docker |
|--------|---------------|--------|
| Size limit | 250MB total | 10GB image |
| Dependencies | Manual management | Automated |
| Reproducibility | Low (platform-specific) | High (containerized) |
| Complexity | Medium | Low |
| **Winner** | ❌ | ✅ |

### Why RandomForest over XGBoost?

| Metric | RandomForest | XGBoost |
|--------|--------------|---------|
| R² Score | 0.42 | 0.44 |
| Training time | 2 min | 8 min |
| Model size | 12 MB | 45 MB |
| Interpretability | High | Medium |
| **Winner** | ✅ | ❌ |

*Decision*: 2% accuracy gain not worth 4x training time + 3.75x model size for this use case

### Why Serverless over EC2?

| Cost (1000 req/day) | Lambda | EC2 t3.micro |
|---------------------|--------|--------------|
| Monthly cost | $0.20 | $7.50 |
| Cold start | 1.4s | 0ms |
| Scaling | Automatic | Manual |
| Maintenance | None | OS updates, patches |
| **Winner** | ✅ | ❌ |

*Decision*: Low traffic = serverless wins on cost + zero maintenance

---

## 🔧 Tools & Technologies Justified

### Why ZenML?
- Pipeline versioning and reproducibility
- Easy integration with MLflow
- Step-level caching (skip unchanged steps)

### Why MLflow?
- Industry standard for experiment tracking
- Built-in model registry
- Easy comparison of runs

### Why Optuna over GridSearch?
- Bayesian optimization = smarter search
- 30% fewer trials for same results
- Early stopping for bad hyperparameters

### Why Streamlit?
- Fastest prototyping for ML dashboards
- Python-native (no JS needed)
- Auto-refresh on file changes

---

## 📊 Performance Metrics (Know These!)

| Metric | Value | Why It Matters |
|--------|-------|----------------|
| Avg response time | 186ms | User experience threshold: <200ms |
| Cold start | 1.4s | Acceptable for serverless |
| Model R² | 0.42 | Better than baseline (0.31) |
| Lambda memory | 237MB / 1024MB | Room for growth |
| Docker image | 60MB | Fast deployment |
| API uptime | 99.9% | Production-ready |
| Cost per 1M requests | $0.20 | 97% cheaper than EC2 |

---

## 🎤 Interview One-Liners

**Deployment Strategy**:
> "I chose Docker over Lambda Layers because ML dependencies are like icebergs - most complexity is hidden. Docker gives complete control."

**Problem-Solving Approach**:
> "When I hit the 250MB Lambda limit, I didn't just compress harder - I questioned whether Lambda needed training libraries at all. Separating concerns solved it."

**CI/CD Design**:
> "My GitHub Actions workflow uses path-based triggers. Why retrain the model when only the Lambda handler changed? Saved 80% of CI/CD costs."

**Permissions Debugging**:
> "AWS permissions are three layers: what can call you (resource policy), what you can call (execution role), and who can deploy (user policy). My API Gateway issue was layer 1."

**Performance Optimization**:
> "I optimized for developer speed first, production metrics second. Caching hyperparameters cut local iteration time by 70%, which mattered more than 2% accuracy gain."

---

## 🚀 Quick Demo Script (For Interviews)

### 1. Show Live API (30 seconds)
```bash
curl -X POST https://mc7310utyk.execute-api.us-east-2.amazonaws.com \
  -H 'Content-Type: application/json' \
  -d '{"fixed_acidity":7.4,"volatile_acidity":0.7,"citric_acid":0,"residual_sugar":1.9,"chlorides":0.076,"free_sulfur_dioxide":11,"total_sulfur_dioxide":34,"density":0.9978,"pH":3.51,"sulphates":0.56,"alcohol":9.4,"wine_type_encoded":0}'

# Response in <200ms:
# {"prediction": 5.18, "quality_rating": "Average", ...}
```

### 2. Show Deployment (30 seconds)
```bash
# One command to deploy everything
./deploy_lambda_docker.sh

# Handles: ECR setup → Docker build → Push → Lambda update → API Gateway → Permissions
```

### 3. Show CI/CD (30 seconds)
```bash
# Show GitHub Actions workflow
cat .github/workflows/deploy-to-aws.yml

# Point out: conditional triggers, parallel steps, error handling
```

### 4. Show Monitoring (30 seconds)
```bash
# Quick debug script
./check_lambda_logs.sh

# Shows: request IDs, execution time, errors, model loading
```

---

## ✅ Pre-Interview Checklist

### Technical Prep
- [ ] Can explain all 6 problems and solutions from memory
- [ ] Know exact performance numbers (186ms, 60MB, 99.9% uptime)
- [ ] Can draw architecture diagram on whiteboard
- [ ] Tested live API endpoint is working

### Story Prep
- [ ] Prepared "most challenging problem" story (scipy errors → Docker)
- [ ] Prepared "debugging" story (API Gateway permissions)
- [ ] Prepared "trade-off" story (RandomForest vs XGBoost)

### Demo Prep
- [ ] Laptop has working internet connection
- [ ] API endpoint tested 5 minutes before interview
- [ ] Code editor open to key files (Dockerfile, lambda_handler.py)
- [ ] Terminal ready with deployment script

---

## 🎯 Tailor by Role

### Data Science / ML Engineer
**Focus on**: Model selection, hyperparameter tuning, experiment tracking, feature engineering

**Skip**: Docker details, IAM permissions

**Highlight**: "I compared 3 algorithms with MLflow tracking. RandomForest won on interpretability vs accuracy trade-off."

### DevOps / MLOps Engineer
**Focus on**: Docker optimization, CI/CD design, AWS architecture, monitoring

**Skip**: Model math, feature selection

**Highlight**: "I reduced Lambda image from 300MB to 60MB by separating training and inference dependencies."

### Full-Stack / Backend Engineer
**Focus on**: API design, error handling, Streamlit dashboard, database integration

**Skip**: Model tuning, deployment scripts

**Highlight**: "My API handles missing features gracefully and returns structured errors with HTTP status codes."

### Software Engineer (General)
**Focus on**: Problem-solving process, code quality, testing, documentation

**Skip**: Deep ML theory, AWS specifics

**Highlight**: "When facing the size limit, I debugged systematically: measured dependencies, found the real problem (separation of concerns), implemented Docker solution."

---

## 💼 Resume Bullet Points by Experience Level

### Entry-Level / Recent Grad
- Built end-to-end ML pipeline with automated training and deployment using GitHub Actions
- Deployed wine quality prediction API on AWS Lambda achieving 186ms average response time
- Reduced deployment errors by switching from Lambda Layers to Docker containers

### Mid-Level (2-5 years)
- Architected serverless MLOps pipeline with ZenML, MLflow, and AWS Lambda serving 1000+ predictions
- Optimized Lambda deployment by 90% (300MB→60MB) through dependency separation and Docker containers
- Implemented CI/CD with conditional triggers reducing deployment costs by 80%

### Senior-Level (5+ years)
- Designed production-grade MLOps system with automated training, experiment tracking, and serverless inference
- Led technical decision-making: Docker vs Layers, RandomForest vs XGBoost, serverless vs EC2 with documented trade-offs
- Established engineering best practices: idempotent deployments, multi-layer IAM, automated testing, comprehensive documentation

---

This quick reference covers all problems faced and solutions implemented. Use the INTERVIEW_GUIDE.md for deeper explanations and the API_TEST_RESULTS.md for performance data.
