import os


def beep():
    try:
        os.system('play -n synth 0.5 sine 1000 gain -10 > /dev/null 2>&1')
    except:
        print('Beep failed, please install sox with')
        print('sudo apt-get install sox')


if __name__ == '__main__':
    beep()
