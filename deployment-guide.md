# MLOps Deployment Guide

This guide explains how to deploy your MLOps stack (ZenML + MLflow) using Docker Compose.

## Architecture

The deployment includes:
- **PostgreSQL**: Database backend for MLflow tracking
- **MinIO**: S3-compatible object storage for artifacts
- **MLflow Server**: Experiment tracking and model registry
- **ZenML Server**: Pipeline orchestration and management
- **Model Server**: Production model serving endpoint

## Prerequisites

- Docker and Docker Compose installed
- At least 4GB RAM available
- Ports 5000, 5432, 8000, 8080, 9000, 9001 available

## Quick Start

### 1. Setup Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and change the default passwords
nano .env
```

### 2. Start the Stack

```bash
# Build and start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### 3. Access Services

After starting, you can access:

- **MLflow UI**: http://localhost:5000
- **ZenML Dashboard**: http://localhost:8080
- **MinIO Console**: http://localhost:9001
- **Model API**: http://localhost:8000

Default credentials:
- MinIO: `minio` / `minio_password`
- ZenML: `admin` / `zenml_password`

### 4. Configure Local ZenML Client

Connect your local ZenML to the deployed server:

```bash
# Connect to ZenML server
zenml connect --url http://localhost:8080 --username admin --password zenml_password

# Register MLflow experiment tracker
zenml experiment-tracker register mlflow_tracker --flavor=mlflow --tracking_uri=http://localhost:5000

# Create a new stack
zenml stack register deployed_stack \
  -o default \
  -a default \
  -e mlflow_tracker

# Set as active stack
zenml stack set deployed_stack
```

### 5. Run Your Pipeline

```bash
# Run the deployment pipeline
python run_deployment.py --config deploy_and_predict
```

## Production Deployment

### Security Considerations

1. **Change Default Passwords**: Update all passwords in `.env`
2. **Enable HTTPS**: Use a reverse proxy (nginx/traefik) with SSL certificates
3. **Network Security**: Restrict port access using firewall rules
4. **Database Backups**: Set up automated PostgreSQL backups
5. **Secrets Management**: Use Docker secrets or external secret managers

### HTTPS Setup with Nginx

Create `nginx.conf`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    location /mlflow/ {
        proxy_pass http://mlflow:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /zenml/ {
        proxy_pass http://zenml:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Scaling

To scale the model server:

```bash
# Scale model server to 3 instances
docker-compose up -d --scale model-server=3

# Use nginx for load balancing
```

## Monitoring

### View Service Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f mlflow
docker-compose logs -f zenml
```

### Resource Monitoring

```bash
# Container resource usage
docker stats

# Disk usage
docker system df
```

## Backup and Recovery

### Backup PostgreSQL Database

```bash
# Create backup
docker-compose exec postgres pg_dump -U mlflow mlflow > backup.sql

# Restore backup
docker-compose exec -T postgres psql -U mlflow mlflow < backup.sql
```

### Backup MinIO Data

```bash
# Export MinIO data
docker-compose exec minio mc mirror /data /backup
```

### Backup ZenML Data

```bash
# Backup ZenML database
docker cp zenml-server:/zenml/zenml.db ./zenml-backup.db
```

## Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs

# Restart services
docker-compose restart

# Rebuild containers
docker-compose up -d --build --force-recreate
```

### Connection Issues

```bash
# Check network
docker network inspect fcc_mlops_project_mlops-network

# Test connectivity
docker-compose exec mlflow curl http://postgres:5432
```

### Storage Issues

```bash
# Clean up old data
docker-compose down -v

# Remove unused volumes
docker volume prune
```

## Stopping and Cleanup

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes all data)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

## Cloud Deployment Options

### AWS Deployment

1. **ECS/Fargate**: Deploy containers using AWS ECS
2. **RDS**: Use RDS PostgreSQL instead of containerized DB
3. **S3**: Use S3 instead of MinIO
4. **ALB**: Use Application Load Balancer for HTTPS and routing

### GCP Deployment

1. **Cloud Run**: Deploy containers serverlessly
2. **Cloud SQL**: Managed PostgreSQL
3. **Cloud Storage**: Replace MinIO with GCS
4. **Cloud Load Balancing**: HTTPS and routing

### Azure Deployment

1. **Container Instances**: Deploy containers
2. **Azure Database**: Managed PostgreSQL
3. **Blob Storage**: Replace MinIO
4. **Application Gateway**: HTTPS and routing

## Best Practices

1. **Use environment-specific configs**: Separate dev, staging, prod configs
2. **Implement CI/CD**: Automate deployments with GitHub Actions/GitLab CI
3. **Monitor resources**: Use Prometheus + Grafana for monitoring
4. **Regular backups**: Automate database and storage backups
5. **Security scanning**: Scan Docker images for vulnerabilities
6. **Log aggregation**: Use ELK stack or cloud logging services

## Support

For issues or questions:
- ZenML Docs: https://docs.zenml.io
- MLflow Docs: https://mlflow.org/docs/latest/index.html
- Docker Docs: https://docs.docker.com
