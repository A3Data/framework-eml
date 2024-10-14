# Framework EML

## Descrição
Este repositório apresenta um pipeline de Machine Learning completo utilizando o dataset Iris. Ele cobre as etapas de download de dados, pré-processamento, treinamento de modelos e predição. Nesse repositório também estão implementadas as melhores práticas e diversas outras features.

## Índice
1. [Instalação](#instalação)
2. [Estrutura do Repositório](#estrutura-do-repositório)
3. [Configuração](#configuração)
4. [Uso](#uso)
   - [Recuperando os Dados](#recuperando-os-dados)
   - [Preparação de Dados](#preparação-de-dados)
   - [Treinamento do Modelo](#treinamento-do-modelo)
   - [Inferência](#inferência)
5. [Versionamento de Dados](#versionamento-de-dados)
6. [Integração e Entrega Contínua (CI/CD)](#integração-e-entrega-contínua-cicd)
7. [Deploy](#deploy)
8. [Testes](#testes)

## Instalação
Passo a passo para utilizar o repositório e instalar as dependências.

### Requisitos

Antes de começar, certifique-se de ter as seguintes dependências instaladas:

- WSL (caso voce esteja usando Windows):
    - Abra um powershell e execute os comandos abaixo na ordem.
    - `wsl --set-default-version 2`
    - `wsl --install -d Ubuntu`
    - `wsl --set-default Ubuntu`
    - Daqui em diante, execute todos os comandos dentro do terminal do wsl.
- Python 3.10+ - https://www.python.org/downloads/
- VSCode - https://code.visualstudio.com/download
    - O VSCode permite instalar extensões, é recomendado instalar ao menos a extensão que integra o VSCode ao WSL.
    - Cole o seguinte ID na aba de extensões: `ms-vscode-remote.remote-wsl`

### Inicializar o ambiente virtual e instalar dependências

Para configurar o ambiente de desenvolvimento e instalar todas as dependências, utilize o Makefile:
```bash
    make init
```

Este comando executará as seguintes etapas:
- Criará o ambiente virtual
- Instalará o Poetry
- Instalará as dependências do projeto
- Configurará o pre-commit e o DVC

### Entrar no ambiente virtual

Para ativar o ambiente execute o comando:

```bash
    source .venv/bin/activate
```

A partir daqui você já tem tudo que é necessário para começar a utilizar o repositório. Modifique os arquivos para adequar ao seu cenário, contudo não altere os nomes das funções. Você pode criar novas funções, mas lembre-se de chamar elas no fluxo principal que são as funções com o decorador `@app.command()` nos arquivos dentro da pasta `src/pipelines`.

## Estrutura do repositório
```bash
├── .dvc                                # Pasta para controle de versionamento de dados com DVC
│
├── .github                             # Configurações para o GitHub Actions
│   └── workflows                       # Workflows de CI/CD
│       ├── pipeline_lint.yml           # Pipeline para lint e formatação
│       ├── pipeline_deploy_batch.yml   # Pipeline para deploy em batch
│       └── pipeline_test.yml           # Pipeline para execução de testes
│
├── api                                 # Código da API para interagir com o modelo
│   └── __init__.py                     # Torna o diretório um módulo Python
│
├── artifacts                           # Armazena dados e modelos
│   ├── data                            # Dados organizados em diferentes estágios
│   │   ├── external                    # Dados de fontes de terceiros
│   │   ├── interim                     # Dados intermediários que foram transformados
│   │   ├── processed                   # Conjuntos de dados finais e canônicos para modelagem
│   │   └── raw                         # Dados originais e imutáveis
│   └── models                          # Pasta para armazenar modelos treinados
│
├── config                              # Configurações de nível de projeto
│   ├── __init__.py                     # Torna o diretório um módulo Python
│   └── environments                    # Configurações de ambiente (ex. dotenv, YAML)
│
├── deployment                          # Arquivos relacionados à implantação e DevOps
│   ├── docker                          # Arquivos para construção e gerenciamento de imagens Docker
│   ├── infrastructure                  # Código para gerenciar a infraestrutura do projeto
│   │   └── terraform                   # Arquivos Terraform para provisionamento de infraestrutura
│   ├── pipelines                       # Pipelines de CI/CD
│   └── scripts                         # Scripts de suporte para construção e implantação
│
├── docs                                # Um projeto mkdocs padrão
│
├── notebooks                           # Notebooks Jupyter
│
├── src                                 # Código fonte para desenvolvimento do modelo
│   ├── __init__.py                     # Torna o diretório um módulo Python
│   ├── pipelines                       # Códigos para pipelines de treino, criação de features e predição
│   │   ├── features.py                 # Código para criação de features
│   │   ├── get_data.py                 # Código para recuperar os dados
│   │   ├── predict.py                  # Código para executar inferência com modelos treinados
│   │   └── train.py                    # Código para treinar modelos
│   └── utils                           # Scripts utilitários
│
├── tests                               # Scripts para execução de testes
│
├── ui                                  # Interface de usuário para interagir com a API do modelo
│    ├── __init__.py                    # Torna o diretório um módulo Python
│    ├── static                         # Templates para a interface de usuário
│    └── templates                      # Arquivos estáticos (CSS, JS, imagens)
│
├── .gitignore                          # Lista de arquivos e/ou diretórios que não são armazenados no repositório
├── .pre-commit-config.yaml             # Arquivo de configuração dos hooks de pre-commit
├── dvc.lock                            # Arquivo de controle do DVC
├── dvc.yaml                            # Arquivo de configuração do DVC
├── Makefile                            # Arquivo para automatizar tarefas comuns de desenvolvimento
├── poetry.lock                         # Arquivo de controle de dependências do Poetry
├── pyproject.toml                      # Configuração do projeto e dependências
└── README.md                           # Documentação do repositório
```

## Configuração

O repositório tem o propósito de ser bem generalista, por isso, tem algumas configurações que você pode fazer para adequar o repositório ao seu projeto.

### Arquivos de configurações globais

#### Settings.py
Dentro da pasta `config` há o arquivo `settings.py`, ele pode ser utilizado para criar qualquer variável para ser utilizada em diferentes estágios do pipeline. Por padrão nós já colocamos os caminhos globais das pastas para referenciá-las sempre que necessário. Por estar centralizado nesse arquivo, se for necessário para seu projeto acrescentar outros arquivos ou trocar de lugar os existentes, você pode alterar somente nesse arquivo e todo o código já estará buscando o caminho correto.

#### Configurações por ambiente
Ainda dentro da pasta `config`, note que há 4 outras pastas, cada uma representando um ambiente do projeto (loc, dev, hml e prd). Algumas configurações podem ser distintas para cada um dos cenários, principalmente arquivos .env, .yaml e outros. Por isso, criamos essas pastas.

No repositório há uma ferramenta que utiliza esses arquivos de configuração. A ferramenta `DVC`, utilizada tanto para versionamento de dados, quanto orquestração do pipeline de treino. Essa ferramenta pode receber parâmetros por meio de um arquivo .yaml, há um exemplo na pasta loc.

### Data Version Control (DVC)
Como citado anteriormente, utilizamos o DVC para o versionamento dos dados e também para a orquestração do pipeline. Existem algumas configurações que você pode querer fazer:
1. Dentro da pasta .dvc há um arquivo config. Dentro desse arquivo config há um bucket S3 configurado, ele está na conta da sandbox da A3. O ideal é voce ter uma conta na AWS voltada para seu projeto, e então criar um bucket e colocar a URL dele no lugar. Você também pode colocar o S3 como sendo o repositório padrão, basta trocar a linha `remote = myremote` para `remote = s3bucket`, assim, ao executar o comando `dvc push` ele irá mandar para o S3. Para usar o S3 voce deve configurar suas credenciais da aws (https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html).
2. O dvc.yaml define o pipeline de treino padrão. Ele está configurado para:
    - Executar o script `get_data.py`
    - Usar a saída do `get_data.py` e executar o `features.py`
    - Usar a saída do `features.py` e executar o `train.py`
Então se você deseja alterar esse fluxo, você deve alterar o arquivo dvc.yaml.

### Dependências e pacotes
As bibliotecas necessárias podem ser instaladas e gerenciadas pelo arquivo `pyproject.toml`.

### Makefile
Esse arquivo contém todas as regras para facilitar o uso do repositório, entraremos em mais detalhes no próximo tópico de uso. Por agora, você pode encontrar algumas variáveis no topo do arquivo `Makefile` que podem ser alteradas, mas que devem funcionar perfeitamente da forma que estão.

## Uso


### Recuperando os Dados
Passos para recuperar e carregar os dados.
O script responsável por essa tarefa é o `src/pipelines/get_data.py`. Nele você deve configurar a forma como seus dados vão ser recuperados. Se eles forem um csv fixo, você pode só apagar essa etapa do pipeline do DVC no arquivo dvc.yaml. O importante é manter o nome da função, todo o conteúdo dela, assim como os parâmetros da função podem e devem ser alterados para o seu cenário.

Ao alterar os parâmetros, será necessário trocar no arquivo `dvc.yaml` os parâmetros esperados durante o pipeline de treino.

Caso você queira testar esse script de maneira isolada execute:
```bash
    # Caso você ainda não tenha ativado o ambiente virtual
    source .venv/bin/activate
    # Lembre-se de passar os argumentos, caso haja
    python -m src.pipelines.get_data
```

### Preparação de Dados
Passos para carregar e preparar os dados para uso.
O script responsável por essa tarefa é o `src/pipelines/features.py`. Esse é o script onde irá se concentrar toda a parte do processamento dos dados. Aqui deve estar toda a parte de limpeza e preparação dos dados, assim como a engenharia de features.

Assim como foi feito na recuperação dos dados, se os parâmetros forem alterados o arquivo `dvc.yaml` deve ser modificado para refletir o que foi alterado no arquivo de preparação de dados.

Caso você queira testar esse script de maneira isolada execute:
```bash
    # Caso você ainda não tenha ativado o ambiente virtual
    source .venv/bin/activate
    # Lembre-se de passar os argumentos, caso haja
    python -m src.pipelines.features
```

### Treinamento do Modelo
Instruções para treinar o modelo utilizando o código fonte.
O script responsável por essa tarefa é o `src/pipelines/train.py`. Aqui é onde fica a lógica de treinar o modelo, então é onde você deve ler o dataset que resultou do features e retornar um arquivo do modelo treinado. O dataset da iris lê dados de treino e teste e treina um modelo SVC. Assim como você alterou os outros arquivos para adaptar ao seu projeto, altere aqui também para treinar seu modelo. Reforçando, todo o arquivo pode ser alterado, exceto pelo nome da função principal. E ao terminar as alterações, vá ao arquivo `dvc.yaml` e faça o mesmo.

Caso você queira testar esse script de maneira isolada execute:
```bash
    # Caso você ainda não tenha ativado o ambiente virtual
    source .venv/bin/activate
    # Lembre-se de passar os argumentos, caso haja
    python -m src.pipelines.train
```

### Inferência
Guia para rodar inferências e salvar resultados.
O script da inferência é o `src/pipelines/predict.py`. Diferente dos outros, aqui há duas funções importantes, a `predict` e a `predict_batch`.

A `predict` serve para inferências pontuais, ela será utilizada no deploy online, enquanto que a `predict_batch` serve para a inferências em lote periódicas e será utilizada no deploy batch.

Na `predict` você deve esperar receber os dados e deve retornar o resultado, por outro lado, no `predict_batch` você deve configurar o fluxo que você espera que aconteça no deploy batch. Por exemplo, caso você deseje ler dados de um banco de dados, fazer a inferência e salvar o resultado em um S3, você deve configurar esses 3 passos dentro da função.


Caso você queira testar esse script de maneira isolada execute:
```bash
    # Caso você ainda não tenha ativado o ambiente virtual
    source .venv/bin/activate
    # Lembre-se de passar os argumentos, caso haja
    python -m src.pipelines.predict predict         # Predict individual
    python -m src.pipelines.predict predict-batch   # Predict em lote
```

Como a `predict_batch` pode ser feita de diferentes formas, o arquivo Dockerfile que faz o deploy batch (`deployment/docker/Dockerfile.batch`) também deve ser alterado ligeiramente. Ao final do arquivo, há o seguinte trecho de código:
```dockerfile
ENV BATCH_INPUT_FILE="artifacts/data/raw/batch_data.csv"
ENV BATCH_OUTPUT_FILE="artifacts/data/processed/predicted_data.csv"

# Comando para rodar o script de predição em lotes
CMD ["sh", "-c", "poetry run python -m src.pipelines.predict predict-batch $BATCH_INPUT_FILE --output-file $BATCH_OUTPUT_FILE"]
```

Note que ele está passando dados de entrada e dizendo onde deve ser a saída, mas a lógica que se adequa ao seu projeto será diferente. Por exemplo, caso você não precise passar nenhum argumento, todo esse trecho anterior se transformaria em:
```dockerfile
# Comando para rodar o script de predição em lotes
CMD ["sh", "-c", "poetry run python -m src.pipelines.predict predict-batch"]
```

### Makefile
O projeto inclui um Makefile para facilitar o gerenciamento do ambiente e das dependências. Alguns comandos disponíveis:
```
make install-poetry           Atualiza as dependências no poetry, útil quando alterar bibliotecas em pyproject.toml
make init                     Prepara todo o repositório com o poetry e pre-commit
make clean                    Remove todo o ambiente virtual e desconfigura o pre-commit
make lint                     Lint usando ruff (use `make format` para formatação)
make format                   Formata o código fonte com ruff
make api                      Inicia a API localmente [Docker]
make batch                    Inicia o batch localmente [Docker]
```

## Versionamento de Dados
Explicação de como usar o DVC para versionar datasets e modelos.

### O que é DVC?

O DVC (Data Version Control) é uma ferramenta open-source que facilita o controle de versões de grandes datasets, modelos e pipelines de machine learning. Ele estende o Git para suportar dados e arquivos pesados, permitindo rastrear e gerenciar versões de dados sem armazená-los diretamente no repositório Git.

### O que o DVC pode fazer?

- **Controle de versão de dados e modelos**: Assim como o Git versiona código, o DVC versiona datasets e modelos de machine learning, facilitando a rastreabilidade de experimentos.
- **Gestão de pipelines**: Automatiza o controle e execução de pipelines de ML, garantindo reprodutibilidade dos processos, desde a preparação dos dados até o treinamento de modelos.
- **Integração com Git**: O DVC rastreia os arquivos de grandes volumes (datasets, checkpoints e modelos) e cria "ponteiros" no Git, para que os arquivos em si possam ser armazenados remotamente (S3, Google Drive, etc.), sem sobrecarregar o repositório Git.
- **Colaboração**: Facilita o trabalho em equipe ao gerenciar versões de datasets compartilhados e modelos, garantindo consistência entre membros.
- **Rastreabilidade e reprodutibilidade**: Cada versão dos dados e dos resultados de experimentos pode ser facilmente recuperada e reproduzida.

### DVC no repositório

**1.** O primeiro passo é verificar se o dvc está corretamente instalado.
```bash
# O primeiro passo é verificar se o dvc está corretamente instalado.
dvc --version
```
**2.** Como executar o pipeline de treino
```bash
# Para executar todo o pipeline de treino
dvc repro

# Para executar um único passo você pode passar o nome dele
dvc repro download

# Se voce quiser evitar que ele verifique as dependências voce pode passar a flag -s
dvc repro -s preprocess

# Para mais informações você sempre pode consultar o help
dvc repro --help
```
**2.** Como salvar e recuperar os dados e artefatos na nuvem
```bash
# Após acabar o treino, é importante fazer o push dos artefatos para o S3
dvc push -r s3bucket

# Caso o armazenamento padrão seja o s3 (veja no tópico "Configurações") você pode executar somente
dvc push

# Para baixar os dados
dvc pull -r s3bucket

# Se quiser do armazenamento padrão, basta usar
dvc pull
```
**3.** Como versionar seus modelos e artefatos
```bash
# Antes de começar, lembre de adicionar qualquer artefato que não esteja mapeado no dvc.yaml e não faça parte do pipeline principal
dvc add artifacts/data/raw/dados_nao_mapeados_pelo_pipe.csv

# Ao terminar uma versão e garantir que todos artefatos estão mapeados pelo dvc, faça o commit para o git
git commit -m "mensagem de commit"

# Agora coloque uma tag para se lembrar depois, de preferencia versionamento semantico
git tag -a "v0.1.0" -m "modelo treinado dia 11/10/24 com dataset x"

# Lembre-se de mandar essa tag para o repositório remoto
git push origin tag v0.1.0

# Pronto! Agora você pode sempre voltar a esse ponto usando o comando
git checkout v0.1.0 # Ao usar esse comando, o dvc já trará os artefatos específicos dessa versão, assim como o código do git

# Se você já tiver muitas versões você pode verificá-las com
git tag --list
```

Se quiser fazer alguns outros testes para ver o dvc funcionando organicamente, experimente os passos a seguir com o dataset da iris já configurado:

**1.** Após reproduzir o pipeline com `dvc repro`, experimente modificar os arquivos gerados dentro da pasta `artifacts/data` e execute o `dvc repro` novamente. Você irá notar que ele busca a versão correta do cache, sem a necessidade de rodar de novo.

**2.** Agora tente apagar esses arquivos, até mesmo o modelo em `artifacts/models/model.joblib`. Tudo isso pode ser recuperado usando `dvc pull`. Esse comando busca do storage (normalmente na nuvem) os arquivos e coloca na pasta local, assim como o git faz com o código. Esse repositório tem configurado como padrão o storage local na pasta /tmp/dvcstore, contudo ele tem também configurado um bucket S3 do ambiente de sandbox da A3. Então se você tiver acesso a conta `a3datasandbox` da aws, experimente o comando: `dvc pull -r s3bucket`. Lembrando, voce deve configurar suas credenciais da aws (https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html).

**3.** Tente fazer alterações no modelo, ou nos dados, ou no processamento, contanto que você mantenha a estrutura dos arquivos, o pipeline irá manter as features mencionadas anteriormente. Faça as alterações e rode `dvc repro`

Você pode conseguir mais informações sobre o dvc no link https://dvc.org/doc.

## Deploy
Passos para deploy em batch ou deploy online.

Os deploys só podem ser feitos através dos pipelines do CI/CD do github. Com isso, garantimos segurança e praticidade já que não há necessidade de configurar terraform, docker, aws cli e credenciais. Há somente alguns cuidados e passos necessários para que o deploy seja feito:

- Primeiro, não alterar os nomes das funções, especialmente das de predict, que são as que serão utilizadas enquanto os modelos estiverem sendo servidos na nuvem.

- Se assegurar de que as mudanças feitas nos códigos de inferência em `src/pipelines/predict.py` estejam sendo refletidas nos Dockerfiles, como instruído em `Inferência`.

- Se ficar em dúvida se o deploy vai funcionar, use os comandos do makefile que permitem voce testar localmente. São eles: `make batch` e `make api`. Eles irão rodar um container Docker da mesma forma que será executado na nuvem.

## Integração e Entrega Contínua (CI/CD)
Detalhes dos pipelines no GitHub Actions.

- **Pipeline Lint**: É o pipeline que irá executar todos os passos para garantir a qualidade do código. São os mesmos passos do pré-commit. Ele fica definido no arquivo `.github/workflows/pipeline_lint.yml`.
- **Pipeline Deploy Batch**: É o pipeline que irá fazer o deploy batch. Ele levanta toda a infraestrutura na AWS, constrói a imagem Docker e envia ela para o repositório privado dentro da AWS para ser utlizada pelo ECS. Esse fluxo fica definido em `.github/workflows/pipeline_deploy_batch.yml`. A infraestrutura é constituída pelos seguintes serviços:
    - ECR
    - ECS com Fargate
    - Eventbridge
    - VPC
    - Ela funciona ao enviar as imagens para o ECR, então o Eventbridge agenda uma tarefa no ECS
- **Pipeline Deploy Online**: Pipeline que faz o deploy online. Ele levanta a infraestrutura na AWS, constrói a imagem Docker e envia ela para o repositório, da mesma forma que o deploy batch. Contudo, ele utiliza como infraestrutura uma AWS Lambda e também um API Gateway para que o endpoint possa ser acessado de qualquer lugar da internet. Se esse NÃO for seu caso, podemos te ajudar a remover essa parte e deixar o endpoint privado.
- **Pipeline Test**: Esse pipeline executa todos os testes definidos dentro da pasta `tests` na raiz do projeto. É utilizado a biblioteca pytest. Há 4 testes nesse caso de uso de exemplo, eles são mais específicados a seguir.

## Testes
Instruções para rodar testes de unidade e integrados.

No exemplo do repositório há 4 testes sendo feitos:
- Testa se o modelo salva corretamente
- Testa se os dados são carregados corretamente
- Testa o pré-processamento e verifica se o dado de treino tem a coluna alvo
- Testa o pré-processamento e verifica se ele levanta um erro ao tentar carregar um arquivo inexistente.

É importante adaptar os testes para o seu cenário. Esse comando executa todos os testes dentro da pasta `tests`, então sinta-se livre para criar quantos testes você achar necessário e lembre-se de alterar os existentes.

A documentação da biblioteca de testes que utilizamos é a seguinte: https://docs.pytest.org/en/stable/

Para executar os testes fora do pipeline de CI/CD, use:

```bash
# Comando para rodar testes
pytest --cov=.
```

## Boas Práticas para Commits com Pré-commit

- Durante o commit, o Pré-commit verifica e corrige a formatação do código, mas não inclui essas alterações automaticamente no commit. É necessário executar `git add` novamente para registrar essas modificações. O Git não faz isso automaticamente para que você tenha controle total sobre o que será comitado. Então, se ao tentar dar commit aparecer um erro, verifique se não há arquivos modificados pelo pré-commit que precisam ser adicionados ao commit.