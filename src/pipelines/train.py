import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import f1_score, classification_report
from sklearn.model_selection import KFold, cross_val_score
import joblib
from pathlib import Path
import typer
from config.settings import PROCESSED_DATA_DIR, MODELS_DIR

app = typer.Typer()


def load_data(train_file: str, test_file: str):
    """
    Carrega os dados de treino e teste a partir de arquivos CSV.

    Args:
        train_file (str): Caminho para o arquivo CSV contendo os dados de treino.
        test_file (str): Caminho para o arquivo CSV contendo os dados de teste.

    Returns:
        tuple: DataFrames com features e alvos para os dados de treino e teste.
    """
    train_data = pd.read_csv(train_file)
    test_data = pd.read_csv(test_file)

    X_train = train_data.drop("species", axis=1)
    y_train = train_data["species"]

    X_test = test_data.drop("species", axis=1)
    y_test = test_data["species"]

    return X_train, y_train, X_test, y_test


def train_model(X_train, y_train):
    """
    Treina um modelo de classificação SVC com validação cruzada (5-fold).

    Args:
        X_train (pd.DataFrame): Conjunto de features para o treino.
        y_train (pd.Series): Conjunto de rótulos (alvos) para o treino.

    Returns:
        SVC: O modelo treinado.
    """
    model = SVC(gamma="auto", random_state=42)

    # Cross-Validation com 5 folds
    kfold = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(
        model, X_train, y_train, cv=kfold, scoring="f1_weighted"
    )

    typer.echo(f"Scores de Cross-Validation (5-Folds): {cv_scores}")
    typer.echo(f"Média de F1-score: {cv_scores.mean() * 100:.2f}%")

    # Treinar o modelo nos dados completos
    model.fit(X_train, y_train)

    return model


def evaluate_model(model, X_test, y_test):
    """
    Avalia o modelo treinado nos dados de teste e exibe a acurácia e o relatório de classificação.

    Args:
        model: O modelo treinado.
        X_test (pd.DataFrame): Conjunto de features para o teste.
        y_test (pd.Series): Conjunto de rótulos para o teste.

    Returns:
        None
    """
    # Fazer previsões nos dados de teste
    y_pred = model.predict(X_test)

    # Avaliar a acurácia
    score = f1_score(y_test, y_pred, average="weighted")
    typer.echo(f"F1-score do modelo: {score * 100:.2f}%")

    # Exibir o relatório de classificação
    typer.echo("Relatório de Classificação:")
    typer.echo(classification_report(y_test, y_pred))


def save_model(model, output_file: str):
    """
    Salva o modelo treinado em um arquivo.

    Args:
        model: O modelo treinado a ser salvo.
        output_file (str): Caminho para salvar o modelo serializado.

    Returns:
        None
    """
    joblib.dump(model, output_file)
    typer.echo(f"Modelo salvo em: {output_file}")


@app.command()
def train(train_file: str = None, test_file: str = None, output_file: str = None):
    """
    Função principal para treinar e salvar o modelo de classificação.

    Args:
        train_file (str, optional): Caminho para o arquivo CSV de treino. Usa valor padrão se não fornecido.
        test_file (str, optional): Caminho para o arquivo CSV de teste. Usa valor padrão se não fornecido.
        output_file (str, optional): Caminho para salvar o modelo treinado. Usa valor padrão se não fornecido.

    Returns:
        None
    """
    # Definir caminhos padrão para os arquivos
    if train_file is None:
        train_file = PROCESSED_DATA_DIR / "train_data.csv"
    if test_file is None:
        test_file = PROCESSED_DATA_DIR / "test_data.csv"
    if output_file is None:
        output_file = MODELS_DIR / "model.joblib"

    # Garantir que o diretório para o modelo exista
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Carregar dados
    X_train, y_train, X_test, y_test = load_data(train_file, test_file)

    # Treinar modelo
    model = train_model(X_train, y_train)

    # Avaliar o modelo
    evaluate_model(model, X_test, y_test)

    # Salvar o modelo treinado
    save_model(model, output_file)


if __name__ == "__main__":
    app()
