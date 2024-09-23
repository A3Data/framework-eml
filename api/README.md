# Guia do Usuário API

1. Certifique-se de ter o ambiente virtual ativado.
2. Instale as dependências usando o Poetry.
3. Navegue até a pasta principal do repositório.
4. Execute a API com o comando:

   ```bash
   python -m api.app.main
   ```

A API começará a rodar em [http://127.0.0.1:8000](http://127.0.0.1:8000) por padrão. Você pode usar ferramentas como curl, Postman ou um script Python para interagir com os endpoints.

Além disso, você pode acessar a documentação da API em [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs), que é gerada automaticamente pelo FastAPI.

## Endpoints da API

### 1. `/predict` (POST)

Prevê a espécie de uma flor de íris com base em uma única amostra de entrada.

**Solicitação:** Informe os valores neste modelo:

```json
{
  "sepal_length": 0,
  "sepal_width": 0,
  "petal_length": 0,
  "petal_width": 0
}
```

### 2. `/predict-batch` (POST)

Processa um arquivo CSV contendo várias amostras para previsões em lote.

**Solicitação:** Carregue um arquivo CSV com as seguintes colunas:

- `sepal_length`
- `sepal_width`
- `petal_length`
- `petal_width`

### 3. `/evaluate` (POST)

Processa um arquivo CSV e avalia previsões em relação a rótulos verdadeiros.

**Solicitação:** Carregue um arquivo CSV com as mesmas colunas acima, mais:

- `species` (o verdadeiro rótulo para avaliação)

## Estrutura do Código

- **main.py**: O ponto de entrada do aplicativo, inicializa o aplicativo FastAPI e inclui o roteador para manipular solicitações.
- **routes.py**: Contém as definições para os endpoints da API, manipulando solicitações de previsões e avaliações.
- **schemas.py**: Define os modelos de dados para validação de entrada e saída usando Pydantic.