import os
import ctypes


def app():
    file_dir = os.getcwd()
    filepath_destination = file_dir + '/Data'
    if len(os.listdir(filepath_destination)) != 0:
        ctypes.windll.user32.MessageBoxW(0, "В папке 'Data' содержатся файлы, удалите перед началом загрузки!",
                                         "Внимание!!!!", 1)
        exit()
    if len(os.listdir(file_dir + '/Ishodnik')) > 1:
        ctypes.windll.user32.MessageBoxW(0, "В папке 'Ishodnik' содержатся несколько файлов, удалите все лишние файлы!",
                                         "Внимание!!!!", 1)
        exit()
    elif len(os.listdir(file_dir + '/Ishodnik')) == 0:
        ctypes.windll.user32.MessageBoxW(0, "В папке 'Ishodnik' нет файлов, поместите туда файл для скачивания!",
                                         "Внимание!!!!", 1)
        exit()
    ishodnik = file_dir + "/Ishodnik/" + os.listdir(file_dir + '/Ishodnik')[0]


    os.system('wget --directory-prefix=' + filepath_destination + ' --load-cookies ' + file_dir + '/urs_cookies --save-cookies ' + file_dir + '/urs_cookies --auth-no-challenge=on --keep-session-cookies --user=vgophap --password=adiletI1 --content-disposition -i ' + ishodnik)
    print()
    print()
    print()
    print('*************** ЗАГРУЗКА ЗАВЕРШЕНА *******************')
    input('НАЖМИТЕ ЛЮБУЮ КНОПКУ ЧТОБЫ ЗАКРЫТЬ ПРОГРАММУ')


if __name__ == "__main__":
    app()
