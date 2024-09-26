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

## Passo a Passo para preparar o ambiente e executar treino

### 1. Inicializar o ambiente virtual e instalar dependências

Para configurar o ambiente de desenvolvimento e instalar todas as dependências, utilize o Makefile:
```
    make init
```

Este comando executará as seguintes etapas:
- Criará o ambiente virtual
- Instalará o Poetry
- Instalará as dependências do projeto
- Configurará o pre-commit e o DVC

### 2. Entrar no ambiente virtual

Para ativar o ambiente execute o comando:

```
    source venv/bin/activate
```

### 3. Instale os pacotes do projeto

Para instalar os pacotes do projeto use:
```
    poetry install
```

### 4. Reproduzir o pipeline

Agora com os pacotes instalados você pode reproduzir o pipeline padrão de treino.

Use a ferramenta DVC (Data Version Control) para reproduzir o pipeline:
```
    dvc repro
```

O pipeline fica definido em dvc.yaml. Neste exemplo está definido lá para:
1. **Baixar os dados** - Os dados serão salvos no diretório `artifacts/data/raw/data.csv`.
2. **Processar os dados** - Os dados processados serão salvos no diretório `artifacts/data/processed/train_data.csv` e `artifacts/data/processed/test_data.csv`
3. **Treinar o modelo** - O modelo é salvo em `artifacts/models/model.joblib`

O dvc é capaz de fazer o rastreamento dos arquivos que servem de entrada e de saída de cada passo do pipeline. E por isso, se voce executar o comando de novo, se nenhum arquivo sofreu alteração (inclusive os de código) ele não irá rodar novamente. Caso alguma alteração seja detectada, ele irá reproduzir do momento da alteração em diante (e.g., se alterar o processamento dos dados, ele não irá baixar os dados novamente, mas irá treinar um novo modelo).

### 5. Fazer previsões

Você pode realizar previsões de duas formas:

#### Previsão em batch

Para realizar previsões em batch utilizando um arquivo CSV de entrada:

    python -m src.pipelines.predict predict-batch caminho/para/arquivo.csv

#### Previsão via linha de comando

Para realizar previsões passando as features diretamente pela linha de comando:

    python -m src.pipelines.predict predict 5.1 3.5 1.4 0.2

## Features do repositório

### DVC

#### O que é DVC?

O DVC (Data Version Control) é uma ferramenta open-source que facilita o controle de versões de grandes datasets, modelos e pipelines de machine learning. Ele estende o Git para suportar dados e arquivos pesados, permitindo rastrear e gerenciar versões de dados sem armazená-los diretamente no repositório Git.

#### O que o DVC pode fazer?

- **Controle de versão de dados e modelos**: Assim como o Git versiona código, o DVC versiona datasets e modelos de machine learning, facilitando a rastreabilidade de experimentos.
- **Gestão de pipelines**: Automatiza o controle e execução de pipelines de ML, garantindo reprodutibilidade dos processos, desde a preparação dos dados até o treinamento de modelos.
- **Integração com Git**: O DVC rastreia os arquivos de grandes volumes (datasets, checkpoints e modelos) e cria "ponteiros" no Git, para que os arquivos em si possam ser armazenados remotamente (S3, Google Drive, etc.), sem sobrecarregar o repositório Git.
- **Colaboração**: Facilita o trabalho em equipe ao gerenciar versões de datasets compartilhados e modelos, garantindo consistência entre membros.
- **Rastreabilidade e reprodutibilidade**: Cada versão dos dados e dos resultados de experimentos pode ser facilmente recuperada e reproduzida.

#### Como testar o poder do DVC

**1.** Após reproduzir o pipeline com `dvc repro`, experimente modificar os arquivos gerados dentro da pasta `artifacts/data` e execute o `dvc repro` novamente. Você irá notar que ele busca a versão correta do cache, sem a necessidade de rodar de novo.

**2.** Agora tente apagar esses arquivos, até mesmo o modelo em `artifacts/models/model.joblib`. Tudo isso pode ser recuperado usando `dvc pull`. Esse comando busca do storage (normalmente na nuvem) os arquivos e coloca na pasta local, assim como o git faz com o código. Esse repositório tem configurado como padrão o storage local na pasta /tmp/dvcstore, contudo ele tem também configurado um bucket S3 do ambiente de sandbox da A3. Então se você tiver acesso a conta `a3datasandbox` da aws, experimente o comando: `dvc pull -r s3bucket`. Lembrando, voce deve configurar suas credenciais da aws (https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html).

**3.** Tente fazer alterações no modelo, ou nos dados, ou no processamento, contanto que você mantenha a estrutura dos arquivos, o pipeline irá manter as features mencionadas anteriormente. Faça as alterações e rode `dvc repro`


## Comandos do Makefile

O projeto inclui um Makefile para facilitar o gerenciamento do ambiente e das dependências. Alguns comandos disponíveis:

- **make init**: Configura o ambiente virtual, instala as dependências e configura o pre-commit e o DVC.
- **make clean**: Remove o ambiente virtual e desinstala o pre-commit.
- **make update**: Atualiza as dependências do Poetry.
- **make lint**: Executa o lint no código-fonte com o Ruff.
- **make format**: Formata o código-fonte com o Ruff.

## Boas Práticas para Commits com Pré-commit

- Durante o commit, o Pré-commit verifica e corrige a formatação do código, mas não inclui essas alterações automaticamente no commit. É necessário executar `git add` novamente para registrar essas modificações. O Git não faz isso automaticamente para que você tenha controle total sobre o que será comitado.