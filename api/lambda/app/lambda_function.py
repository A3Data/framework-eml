import json
import pandas as pd
from src.pipelines.predict import load_model, make_predictions


MODEL_FILE = "artifacts/models/model.joblib"
model = load_model(MODEL_FILE)


def validate_input(item):
    """Valida se o item contém pelo menos um valor e é uma lista com o tamanho correto."""
    if not item or not isinstance(item, list) or len(item) != 4:
        raise ValueError("O item deve ser uma lista com 4 valores.")


def make_prediction(item):
    """Faz previsão com base nos dados de entrada."""
    data = pd.DataFrame(
        [item], columns=["sepal_length", "sepal_width", "petal_length", "petal_width"]
    )
    prediction = make_predictions(model, data)
    return prediction.astype(int).tolist()[0]


def process_event(event):
    """Processa o evento e gera previsões."""
    if isinstance(event, str):
        event = json.loads(event)
    if "body" in event:
        body = json.loads(event["body"])
    else:
        body = event
    predictions = []

    for item in body:
        try:
            validate_input(item)
            prediction = make_prediction(item)
            predictions.append({"prediction": prediction})
        except Exception as e:
            predictions.append({"error": str(e)})
    return predictions


def lambda_handler(event, context):
    """Função principal que recebe o evento e contexto."""
    predictions = process_event(event)
    return {"statusCode": 200, "body": json.dumps(predictions)}
