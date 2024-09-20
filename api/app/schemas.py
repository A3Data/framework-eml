import pandas as pd
from pydantic import BaseModel


class PredictRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

    def to_dataframe(self) -> pd.DataFrame:
        """Prepara os dados como um DataFrame a partir do pedido."""
        return pd.DataFrame(
            [
                [
                    self.sepal_length,
                    self.sepal_width,
                    self.petal_length,
                    self.petal_width,
                ]
            ],
            columns=["sepal_length", "sepal_width", "petal_length", "petal_width"],
        )


class PredictionResponse(BaseModel):
    prediction: int
