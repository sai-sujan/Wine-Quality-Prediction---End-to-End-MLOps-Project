.PHONY: help build up down restart logs clean backup restore

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build all Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d
	@echo "Services started!"
	@echo "MLflow UI: http://localhost:5000"
	@echo "ZenML Dashboard: http://localhost:8080"
	@echo "MinIO Console: http://localhost:9001"
	@echo "Model API: http://localhost:8000"

down: ## Stop all services
	docker-compose down

restart: ## Restart all services
	docker-compose restart

logs: ## Show logs for all services
	docker-compose logs -f

logs-mlflow: ## Show MLflow logs
	docker-compose logs -f mlflow

logs-zenml: ## Show ZenML logs
	docker-compose logs -f zenml

logs-model: ## Show model server logs
	docker-compose logs -f model-server

ps: ## Show running services
	docker-compose ps

clean: ## Stop services and remove volumes (WARNING: deletes data)
	docker-compose down -v
	docker system prune -f

backup: ## Backup databases and storage
	@mkdir -p backups
	@echo "Backing up PostgreSQL..."
	docker-compose exec -T postgres pg_dump -U mlflow mlflow > backups/mlflow-$$(date +%Y%m%d-%H%M%S).sql
	@echo "Backing up ZenML..."
	docker cp zenml-server:/zenml/zenml.db backups/zenml-$$(date +%Y%m%d-%H%M%S).db
	@echo "Backup completed!"

restore: ## Restore from backup (set BACKUP_FILE variable)
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "Error: BACKUP_FILE not set. Usage: make restore BACKUP_FILE=backups/mlflow-20240101.sql"; \
		exit 1; \
	fi
	docker-compose exec -T postgres psql -U mlflow mlflow < $(BACKUP_FILE)
	@echo "Restore completed!"

health: ## Check health of all services
	@echo "Checking service health..."
	@curl -s http://localhost:5000/health && echo "✓ MLflow is healthy" || echo "✗ MLflow is down"
	@curl -s http://localhost:8080/health && echo "✓ ZenML is healthy" || echo "✗ ZenML is down"
	@curl -s http://localhost:9000/minio/health/live && echo "✓ MinIO is healthy" || echo "✗ MinIO is down"

init-minio: ## Initialize MinIO bucket for MLflow
	docker-compose exec minio mc alias set myminio http://localhost:9000 minio minio_password
	docker-compose exec minio mc mb myminio/mlflow
	@echo "MinIO bucket created!"

connect-zenml: ## Connect local ZenML to deployed server
	zenml connect --url http://localhost:8080 --username admin --password zenml_password
	@echo "Connected to ZenML server!"

setup-stack: ## Setup ZenML stack with deployed services
	zenml experiment-tracker register deployed_mlflow --flavor=mlflow --tracking_uri=http://localhost:5000
	zenml stack register deployed_stack -o default -a default -e deployed_mlflow
	zenml stack set deployed_stack
	@echo "ZenML stack configured!"

dev: build up init-minio connect-zenml setup-stack ## Complete development setup
	@echo "Development environment ready!"
	@echo "Run your pipelines with: python run_deployment.py"
