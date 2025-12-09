.PHONY: help build up down logs scale status clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

build: ## Build Docker images
	docker build -f docker/python-etl/Dockerfile -t kettler-python-etl:latest .
	docker build -f docker/r-analysis/Dockerfile -t kettler-r-analysis:latest .

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## View logs (use LOGS_SERVICE=python-etl for specific service)
	docker-compose logs -f $(if $(LOGS_SERVICE),$(LOGS_SERVICE),)

scale-etl: ## Scale ETL service (use REPLICAS=3)
	docker-compose up -d --scale python-etl=$(if $(REPLICAS),$(REPLICAS),3)

scale-analysis: ## Scale R analysis service (use REPLICAS=2)
	docker-compose up -d --scale r-analysis=$(if $(REPLICAS),$(REPLICAS),2)

scale-all: ## Scale all services for parallel execution
	docker-compose up -d --scale python-etl=3 --scale r-analysis=2 --scale vector-api=2

status: ## Show service status
	docker-compose ps

restart: ## Restart all services
	docker-compose restart

clean: ## Remove containers and volumes
	docker-compose down -v

# Kubernetes targets
k8s-deploy: ## Deploy to Kubernetes
	kubectl apply -f kubernetes/persistent-volumes.yaml
	kubectl apply -f kubernetes/python-etl-deployment.yaml
	kubectl apply -f kubernetes/r-analysis-deployment.yaml
	kubectl apply -f kubernetes/vector-api-deployment.yaml

k8s-scale-etl: ## Scale ETL in Kubernetes (use REPLICAS=5)
	kubectl scale deployment python-etl --replicas=$(if $(REPLICAS),$(REPLICAS),5)

k8s-scale-analysis: ## Scale R analysis in Kubernetes (use REPLICAS=4)
	kubectl scale deployment r-analysis --replicas=$(if $(REPLICAS),$(REPLICAS),4)

k8s-status: ## Show Kubernetes pod status
	kubectl get pods -l app=python-etl
	kubectl get pods -l app=r-analysis

k8s-logs: ## View Kubernetes logs (use POD=python-etl-xxx)
	kubectl logs -l app=$(if $(POD),$(POD),python-etl) --tail=100 -f

k8s-delete: ## Delete Kubernetes deployments
	kubectl delete -f kubernetes/python-etl-deployment.yaml
	kubectl delete -f kubernetes/r-analysis-deployment.yaml
	kubectl delete -f kubernetes/vector-api-deployment.yaml

# MCP targets
mcp-list: ## List containers via MCP
	python docker/mcp/docker-mcp-server.py list

mcp-status: ## Get service status via MCP
	python docker/mcp/docker-mcp-server.py status

mcp-scale: ## Scale service via MCP (use SERVICE=python-etl REPLICAS=3)
	python docker/mcp/docker-mcp-server.py scale --service $(if $(SERVICE),$(SERVICE),python-etl) --replicas $(if $(REPLICAS),$(REPLICAS),3)

# Google Drive MCP targets
mcp-drive-list: ## List Google Drive folder contents (use FOLDER_ID=...)
	python scripts/mcp/google_drive_mcp_server.py list --folder-id $(if $(FOLDER_ID),$(FOLDER_ID),1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8)

mcp-drive-download: ## Download Google Drive folder (use FOLDER_ID=... OUTPUT_DIR=...)
	python scripts/mcp/google_drive_mcp_server.py download --folder-id $(if $(FOLDER_ID),$(FOLDER_ID),1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8) --output-dir $(if $(OUTPUT_DIR),$(OUTPUT_DIR),data/drive_downloads) --recursive

mcp-drive-export-doc: ## Export Google Doc (use FILE_ID=... OUTPUT_PATH=... FORMAT=docx)
	python scripts/mcp/google_drive_mcp_server.py export-doc --file-id $(FILE_ID) --output-path $(OUTPUT_PATH) --format $(if $(FORMAT),$(FORMAT),docx)

mcp-drive-export-sheet: ## Export Google Sheet (use FILE_ID=... OUTPUT_PATH=... FORMAT=xlsx)
	python scripts/mcp/google_drive_mcp_server.py export-sheet --file-id $(FILE_ID) --output-path $(OUTPUT_PATH) --format $(if $(FORMAT),$(FORMAT),xlsx)

mcp-tools-list: ## List all available MCP tools
	python3 scripts/mcp/list_mcp_tools.py

# Test targets
test-etl: ## Test ETL pipeline
	docker-compose run --rm python-etl python scripts/etl/etl_pipeline.py

test-analysis: ## Test R analysis
	docker-compose run --rm r-analysis Rscript scripts/analysis/analyze_all_evidence.R

test-api: ## Test Vector API
	curl http://localhost:8000/health

# Development targets
dev-up: ## Start services for development
	docker-compose up

dev-shell-python: ## Open Python container shell
	docker-compose run --rm python-etl /bin/bash

dev-shell-r: ## Open R container shell
	docker-compose run --rm r-analysis /bin/bash
