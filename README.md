# Framework EML

Este repositório apresenta um pipeline de Machine Learning completo utilizando o dataset Iris. Ele cobre as etapas de download de dados, pré-processamento, treinamento de modelos e predição.

## Estrutura do repositório

```
├── api                         # Código da API para interagir com o modelo
│   └── __init__.py             # Torna o diretório um módulo Python
│
├── config                      # Configurações de nível de projeto
│   ├── __init__.py             # Torna o diretório um módulo Python
│   └── environments            # Configurações de ambiente (ex. dotenv, YAML)
│
├── data                        # Organização dos dados
│   ├── external                # Dados de fontes de terceiros
│   ├── interim                 # Dados intermediários que foram transformados
│   ├── processed               # Conjuntos de dados finais e canônicos para modelagem
│   └── raw                     # Dados originais e imutáveis
│
├── deployment                  # Arquivos relacionados à implantação e DevOps
│   ├── docker                  # Arquivos para construção e gerenciamento de imagens Docker
│   ├── infrastructure          # Código para gerenciar a infraestrutura do projeto
│   │   └── terraform           # Arquivos Terraform para provisionamento de infraestrutura
│   ├── pipelines               # Pipelines de CI/CD
│   └── scripts                 # Scripts de suporte para construção e implantação
│
├── docs                        # Um projeto mkdocs padrão
│
├── models                      # Modelos treinados e scripts relacionados
│   ├── __init__.py             # Torna o diretório um módulo Python
│   ├── data                    # Scripts para coleta, leitura e processamento de dados
│   └── trained                 # Modelos treinados e serializados
│
├── notebooks                   # Notebooks Jupyter
│
├── reports                     # Análises e relatórios gerados
│   ├── figures                 # Gráficos e figuras gerados para os relatórios
│   └── html                    # Relatórios gerados em HTML
│
├── src                         # Código fonte para desenvolvimento do modelo
│   ├── __init__.py             # Torna o diretório um módulo Python
│   ├── pipelines               # Códigos para pipelines de treino, criação de features e predição
│   │   ├── features.py         # Código para criação de features
│   │   ├── predict.py          # Código para executar inferência com modelos treinados
│   │   └── train.py            # Código para treinar modelos
│   └── utils                   # Scripts utilitários
│
├── tests                       # Scripts para execução de testes
│
├── ui                          # Interface de usuário para interagir com a API do modelo
│    ├── __init__.py            # Torna o diretório um módulo Python
│    ├── static                 # Templates para a interface de usuário
│    └── templates              # Arquivos estáticos (CSS, JS, imagens)
│
├── .gitignore                  # Lista de arquivos e/ou diretórios que não são armazenados no repositório
├── .pre-commit-config.yaml     # Arquivo de configuração dos hooks de pre-commit
├── LICENSE                     # Licença de código aberto, se aplicável
├── Makefile                    # Arquivo para automatizar tarefas comuns de desenvolvimento
├── pyproject.toml              # Configuração do projeto e dependências
└── README.md                   # Documentação do repositório
```

## Requisitos

Antes de começar, certifique-se de ter as seguintes dependências instaladas:

- Python 3.8+
- Poetry para gerenciamento de dependências

## Passo a Passo para Execução

### 1. Inicializar o ambiente virtual e instalar dependências

Para configurar o ambiente de desenvolvimento e instalar todas as dependências, utilize o Makefile:

    make init

Este comando executará as seguintes etapas:
- Criará o ambiente virtual
- Instalará o Poetry
- Instalará as dependências do projeto
- Configurará o pre-commit e o DVC

### 2. Baixar os dados

Após a configuração, baixe o dataset Iris com o comando:

    python models/data/retrieve_data.py "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

Os dados serão salvos no diretório `data/raw`.

### 3. Pré-processamento de features

Execute o script de pré-processamento para preparar os dados:

    python src/pipelines/features.py

O script processa os dados e os salva em `data/processed`.

### 4. Treinamento do modelo

Treine o modelo utilizando o SVC com validação cruzada (5 k-fold) e faça a avaliação:

    python src/pipelines/train.py

O modelo treinado será salvo no diretório `models/trained`.

### 5. Fazer previsões

Você pode realizar previsões de duas formas:

#### Previsão em batch

Para realizar previsões em batch utilizando um arquivo CSV de entrada:

    python src/pipelines/predict.py predict_batch --input-file caminho/para/arquivo.csv

#### Previsão via linha de comando

Para realizar previsões passando as features diretamente pela linha de comando:

    python src/pipelines/predict.py predict --sepal-length 5.1 --sepal-width 3.5 --petal-length 1.4 --petal-width 0.2

## Comandos do Makefile

O projeto inclui um Makefile para facilitar o gerenciamento do ambiente e das dependências. Alguns comandos disponíveis:

- **make init**: Configura o ambiente virtual, instala as dependências e configura o pre-commit e o DVC.
- **make clean**: Remove o ambiente virtual e desinstala o pre-commit.
- **make update**: Atualiza as dependências do Poetry.
- **make lint**: Executa o lint no código-fonte com o Ruff.
- **make format**: Formata o código-fonte com o Ruff.