from pydantic import BaseModel

class ModelNameConfig(BaseModel):
    """Model config"""
    model_name: str = "LinearRegressionModel"
    fine_tuning: bool = False
