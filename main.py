import sys
from pathlib import Path
import pandas as pd

import utils.args_list as args_list
from core.models import load_model_from_file
from utils.config import BASE_MODEL_PATH
from core.dataloader import load_data, transform_data


def main(data_path: Path):
    print(data_path.absolute())
    data = load_data(data_path)
    data = transform_data(data)
    
    model = load_model_from_file(Path(BASE_MODEL_PATH))
    prediction = model.predict(data)
    print(prediction)

if __name__ == '__main__':
    if any(flag in sys.argv for flag in args_list.HELP_FLAGS):
        print(
            '\nДля генерации предсказаний модели укажите путь к файлу с данными в формате csv',
            'Пример запусука python3 main.py [file_path]\n',
            'Список аргументов для настройки запуска утилиты:',
            '--tune [file_path] - дообучения модели на данных предоставленых в файле file_path',
            sep='\n'
        )
        exit(0)
    if any(flag in sys.argv for flag in args_list.TUNING_FLAGS):
        pass
    if pred_data := Path(sys.argv[1]):
        if not pred_data.exists():
            print('Неверный путь к файлу')
            exit(1)
        main(pred_data)
        exit(0)
    if sys.argv[1:]:
        print('Неизвестные аргументы:', *sys.argv[1:])
        exit(1)

    