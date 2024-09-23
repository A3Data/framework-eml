# Use a imagem base do Python
FROM python:3.10-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Instala o Poetry via pip
RUN pip install poetry

# Copia o arquivo pyproject.toml para instalar dependências
COPY pyproject.toml .

# Instala as dependências do projeto sem utilizar o poetry.lock
RUN poetry lock \
    && poetry install --no-dev

COPY artifacts/ artifacts/
COPY api/ api/
COPY src/ src/
COPY config/ config/

# Expõe a porta 8000 para o servidor FastAPI
EXPOSE 8000

# Comando para rodar a aplicação FastAPI com Uvicorn
CMD ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
