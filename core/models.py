from pathlib import Path
from catboost import CatBoostClassifier

model = CatBoostClassifier()

def load_model_from_file(model_path: Path):
    model.load_model(model_path)
    return model