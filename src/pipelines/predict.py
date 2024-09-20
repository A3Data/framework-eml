import pandas as pd
import joblib
import typer
from sklearn.metrics import classification_report
from config.settings import MODELS_DIR

app = typer.Typer()


def load_model(model_path: str):
    """
    Carrega um modelo treinado a partir de um arquivo.

    Args:
        model_path (str): Caminho para o arquivo do modelo treinado.

    Returns:
        object: O modelo treinado carregado.
    """
    return joblib.load(model_path)


def load_data(file_path: str) -> pd.DataFrame:
    """
    Carrega o dataset a partir de um arquivo CSV.

    Args:
        file_path (str): Caminho para o arquivo CSV que contém o dataset.

    Returns:
        pd.DataFrame: DataFrame contendo o dataset carregado, com as colunas nomeadas.
    """
    column_names = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    df = pd.read_csv(file_path, header=None, names=column_names)
    return df


def make_predictions(model, data: pd.DataFrame):
    """
    Faz previsões a partir de um modelo treinado e dados de entrada.

    Args:
        model: O modelo treinado.
        data (pd.DataFrame): Os dados de entrada para predição.

    Returns:
        pd.Series: As previsões feitas pelo modelo.
    """
    return model.predict(data)


def evaluate_predictions(predictions: pd.Series, true_labels: pd.Series):
    """
    Avalia as previsões do modelo em relação aos rótulos reais.

    Args:
        predictions (pd.Series): As previsões feitas pelo modelo.
        true_labels (pd.Series): Os rótulos reais.

    Returns:
        str: Relatório de classificação.
    """
    return classification_report(
        true_labels, predictions, output_dict=True, zero_division=0
    )


@app.command()
def predict_batch(
    input_file: str = typer.Argument(
        ..., help="Caminho para o arquivo CSV contendo os dados de entrada."
    ),
    model_file: str = typer.Option(
        None, help="Caminho para o arquivo do modelo treinado."
    ),
    output_file: str = typer.Option(None, help="Caminho para salvar as previsões."),
    evaluate: bool = typer.Option(
        False, help="Se verdadeiro, avalia as previsões usando rótulos reais."
    ),
    print_output: bool = typer.Option(
        True, help="Se verdadeiro, imprime as previsões na linha de comando."
    ),
):
    """
    Função principal para carregar dados e modelo, fazer previsões e opcionalmente avaliá-las.

    Args:
        input_file (str): Caminho para o arquivo CSV contendo os dados de entrada.
        model_file (str, optional): Caminho para o arquivo do modelo treinado.
        output_file (str, optional): Caminho para salvar as previsões.
        evaluate (bool, optional): Se verdadeiro, avalia as previsões com base nos rótulos reais.
    """
    # Definir caminho padrão para o modelo se não for fornecido
    if model_file is None:
        model_file = MODELS_DIR / "svc_model.joblib"

    # Carregar o modelo
    typer.echo(f"Carregando o modelo de {model_file}...")
    model = load_model(model_file)

    # Carregar os dados
    typer.echo(f"Carregando os dados de {input_file}...")
    data = load_data(input_file)

    # Se for para avaliar, separar os rótulos reais
    true_labels = None
    if evaluate:
        if "species" not in data.columns:
            raise ValueError(
                "Os dados de entrada devem conter a coluna 'species' para avaliação."
            )
        true_labels = data.pop("species")

    # Fazer previsões
    typer.echo("Fazendo previsões...")
    predictions = make_predictions(model, data)

    # Avaliar previsões, se necessário
    if evaluate and true_labels is not None:
        typer.echo("Avaliando previsões...")
        report = evaluate_predictions(predictions, true_labels)
        typer.echo(report)

    if print_output:
        typer.echo(f"Previsões: {predictions}")

    # Salvar previsões, se necessário
    if output_file:
        typer.echo(f"Salvando previsões em {output_file}...")
        output_df = pd.DataFrame({"prediction": predictions})
        output_df.to_csv(output_file, index=False)
        typer.echo("Previsões salvas com sucesso!")


@app.command()
def predict(
    sepal_length: float = typer.Argument(..., help="Comprimento da sépala."),
    sepal_width: float = typer.Argument(..., help="Largura da sépala."),
    petal_length: float = typer.Argument(..., help="Comprimento da pétala."),
    petal_width: float = typer.Argument(..., help="Largura da pétala."),
    model_file: str = typer.Option(
        None, help="Caminho para o arquivo do modelo treinado."
    ),
):
    """
    Faz predições a partir das features fornecidas diretamente via linha de comando.
    """
    if model_file is None:
        model_file = MODELS_DIR / "svc_model.joblib"

    typer.echo(f"Carregando o modelo de {model_file}...")
    model = load_model(model_file)

    data = pd.DataFrame(
        [[sepal_length, sepal_width, petal_length, petal_width]],
        columns=["sepal_length", "sepal_width", "petal_length", "petal_width"],
    )

    typer.echo("Fazendo predição...")
    prediction = make_predictions(model, data)
    typer.echo(f"Predição: {prediction[0]}")


if __name__ == "__main__":
    app()
