# Define o diretório do ambiente virtual
VENV_DIR = .venv

# Define o nome do comando para o Python
PYTHON = python3
DOCKER_IMAGE_NAME = eml
REPO_NAME = $(DOCKER_IMAGE_NAME)
AWS_REGION = us-east-1
ACCOUNT_ID = $(shell aws sts get-caller-identity --query Account --output text)
REPO_URI = $(ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(REPO_NAME)
API_PORT = 8000
TERRAFORM_BUCKET = eml-terraform-bucket-$(ACCOUNT_ID)


.PHONY: venv
venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Criando o ambiente virtual..."; \
		$(PYTHON) -m venv $(VENV_DIR); \
	else \
		echo "O ambiente virtual já existe."; \
	fi
	@if [ ! -d "artifacts" ]; then \
		echo "Criando pasta para os artefatos (essa pasta não deve ser comitada!)..."; \
		mkdir artifacts; \
	else \
		echo "A pasta de dados já existe."; \
	fi
	@if [ ! -d "/tmp/dvcstore" ]; then \
		echo "Criando temporaria para dvc local (essa pasta não deve ser comitada!)..."; \
		mkdir /tmp/dvcstore; \
	else \
		echo "A pasta temporaria do dvc já existe."; \
	fi


## Atualiza as dependências no poetry, útil quando alterar bibliotecas em pyproject.toml
.PHONY: install-poetry
install-poetry: venv
	@echo "Instalando o Poetry..."
	$(VENV_DIR)/bin/pip install poetry
	$(VENV_DIR)/bin/poetry config virtualenvs.in-project true


.PHONY: install-dependencies
install-dependencies: install-poetry
	@echo "Instalando dependências com o Poetry..."
	$(VENV_DIR)/bin/poetry install


.PHONY: install-pre-commit
install-pre-commit: install-dependencies
	@echo "Instalando hooks de pre-commit"
	$(VENV_DIR)/bin/poetry run pre-commit install --hook-type pre-push --hook-type post-checkout --hook-type pre-commit


## Prepara todo o repositório com o poetry e pre-commit
.PHONY: init
init: install-pre-commit
	$(VENV_DIR)/bin/poetry run dvc remote add -f s3bucket s3://framework-eml-a3data/dvc/
	$(VENV_DIR)/bin/poetry run dvc remote add -d -f myremote /tmp/dvcstore


## Remove todo o ambiente virtual e desconfigura o pre-commit
.PHONY: clean
clean:
	@echo "Removendo pre-commit..."
	$(VENV_DIR)/bin/poetry run pre-commit uninstall
	$(VENV_DIR)/bin/poetry run pre-commit clean
	@echo "Removendo poetry cache"
	$(VENV_DIR)/bin/poetry cache clear --all -n .
	@echo "Removendo o ambiente virtual..."
	rm -rf $(VENV_DIR)


## Lint usando ruff (use `make format` para formatação)
.PHONY: lint
lint:
	$(VENV_DIR)/bin/poetry run ruff check


## Formata o código fonte com ruff
.PHONY: format
format:
	$(VENV_DIR)/bin/poetry run ruff format


.PHONY: build-api-image
build-api-image:
	docker build -t $(DOCKER_IMAGE_NAME)-api -f deployment/docker/Dockerfile.api .


.PHONY: build-batch-image
build-batch-image:
	docker build -t $(DOCKER_IMAGE_NAME)-batch -f deployment/docker/Dockerfile.batch .


## Inicia a API localmente [Docker]
.PHONY: api
api: build-api-image
	@echo "Lançando a API localmente..."
	docker run -p $(API_PORT):$(API_PORT) $(DOCKER_IMAGE_NAME)-api:latest


## Inicia o batch localmente [Docker]
.PHONY: batch
batch: build-batch-image
	@echo "Lançando o batch localmente..."
	docker run $(DOCKER_IMAGE_NAME)-batch:latest


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Comandos disponíveis:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)