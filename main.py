import sys
import utils.args_list as args_list
from pathlib import Path

def main(data: Path):
    print(data)
    

if __name__ == '__main__':
    interval = '-t3'

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

    