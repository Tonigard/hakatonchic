import sys
import utils.args_list as args_list

def main(interval: str):
    print(interval)
    

if __name__ == '__main__':
    interval = '-t3'

    if any(flag in sys.argv for flag in args_list.HELP_FLAGS):
        print('Это справка по работу с данной утилитой')
        exit(0)
    if any(flag in sys.argv for flag in args_list.PREDICTION_INTERVAL_FLAGS):
        interval_args = [flag for flag in sys.argv if flag in args_list.PREDICTION_INTERVAL_FLAGS]
        interval = interval_args[0]
        for arg in interval_args:
            sys.argv.remove(arg)
    if sys.argv[1:]:
        print('Неизвестные аргументы:', *sys.argv[1:])
        exit(1)

    main(
        interval=interval
    )