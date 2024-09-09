# Define o diretório do ambiente virtual
VENV_DIR = venv

# Define o nome do comando para o Python
PYTHON = python3

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

.PHONY: install-poetry
install-poetry: venv
	@echo "Instalando o Poetry..."
	$(VENV_DIR)/bin/pip install poetry

.PHONY: install-dependencies
install-dependencies: install-poetry
	@echo "Instalando dependências com o Poetry..."
	$(VENV_DIR)/bin/poetry lock
	$(VENV_DIR)/bin/poetry install

.PHONY: install-pre-commit
install-pre-commit: install-dependencies
	@echo "Instalando hooks de pre-commit"
	$(VENV_DIR)/bin/poetry run pre-commit install

## [PADRÃO] Prepara todo o repositório com o poetry e pre-commit
.PHONY: init
init: install-pre-commit
	$(VENV_DIR)/bin/poetry run dvc remote add -d -f myremote /tmp/dvcstore

## Remove todo o ambiente virtual e desconfigura o pre-commit
.PHONY: clean
clean:
	@echo "Removendo pre-commit..."
	$(VENV_DIR)/bin/poetry run pre-commit uninstall
	$(VENV_DIR)/bin/poetry run pre-commit clean
	@echo "Removendo o ambiente virtual..."
	rm -rf $(VENV_DIR)

## Atualiza as dependências no poetry, útil quando alterar bibliotecas em pyproject.toml
.PHONY: update
update:
	@echo "Atualizando pacotes com poetry"
	$(VENV_DIR)/bin/poetry lock
	$(VENV_DIR)/bin/poetry install

## Lint usando ruff (use `make format` para formatação)
.PHONY: lint
lint:
	$(VENV_DIR)/bin/poetry run ruff check

## Formata o código fonte com ruff
.PHONY: format
format:
	$(VENV_DIR)/bin/poetry run ruff format


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