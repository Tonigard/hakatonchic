import sys
import utils.args_list as args_list

def main(args: list[any]):
    if any(flag in args for flag in args_list.HELP_FLAGS):
        print('Это справка по работу с данной утилитой')
    

if __name__ == '__main__':
    main(sys.argv[1:])