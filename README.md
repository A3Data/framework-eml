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

URL dos dados iris para teste: https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data