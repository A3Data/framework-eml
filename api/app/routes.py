import pandas as pd
from fastapi import APIRouter, HTTPException, File, UploadFile
from .schemas import PredictRequest, PredictionResponse
from config.settings import MODELS_DIR
from src.pipelines.predict import load_model, make_predictions, evaluate_predictions
from io import StringIO
import json

router = APIRouter()
model_path = MODELS_DIR / "svc_model.joblib"


@router.post("/predict", response_model=PredictionResponse)
async def predict(input: PredictRequest):
    data = input.to_dataframe()

    try:
        model = load_model(model_path)
        prediction = make_predictions(model, data)
        result = int(prediction[0])
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao fazer a previsão: {str(e)}"
        )

    return PredictionResponse(prediction=result)


@router.post("/predict-batch", response_model=dict)
async def predict_batch(file: UploadFile = File(...)):
    """Faz previsões em lote a partir de um arquivo CSV.

    O arquivo CSV deve conter as seguintes colunas:
    - sepal_length: Comprimento da sépala.
    - sepal_width: Largura da sépala.
    - petal_length: Comprimento da pétala.
    - petal_width: Largura da pétala.
    """
    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))
        model = load_model(model_path)

        predictions = make_predictions(model, df)

        return {"predictions": predictions.tolist()}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar o arquivo: {str(e)}"
        )


@router.post("/evaluate", response_model=dict)
async def predict_batch_with_evaluation(file: UploadFile = File(...)):
    """Faz previsões em lote a partir de um arquivo CSV.

    O arquivo CSV deve conter as seguintes colunas:
    - sepal_length: Comprimento da sépala.
    - sepal_width: Largura da sépala.
    - petal_length: Comprimento da pétala.
    - petal_width: Largura da pétala.
    - species: Rótulo verdadeiro da espécie (para avaliação).
    """
    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))
        model = load_model(model_path)

        if "species" not in df.columns:
            raise HTTPException(
                status_code=400,
                detail="Os dados devem conter a coluna 'species' para avaliação.",
            )

        true_labels = df.pop("species")
        predictions = make_predictions(model, df)

        report_dict = evaluate_predictions(predictions, true_labels)
        report = json.dumps(report_dict, indent=4)
        return {
            "evaluation_report": json.loads(report),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar o arquivo: {str(e)}"
        )
