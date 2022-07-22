import os
import sys
import subprocess
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QRunnable, QThreadPool
from PyQt5.QtWidgets import QFileDialog, QDesktopWidget, QCheckBox, QGridLayout, QTabWidget, QApplication, QWidget, QLabel, \
    QPushButton, QLineEdit, QComboBox, QMessageBox



class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        self.lab1 = QLabel('Логин:', self)
        self.lab1.move(50, 20)
        self.text_login = QLineEdit(self)
        self.text_login.move(50, 40)
        self.text_login.setText('vgophap')
        self.lab2 = QLabel('Пароль', self)
        self.lab2.move(50, 60)

        self.text_pass = QLineEdit(self)
        self.text_pass.move(50, 80)
        self.text_pass.setText('adiletI1')
        self.btn_notepad_choose = QPushButton('Выбрать документ', self)
        self.btn_notepad_choose.move(50, 120)
        self.btn_notepad_choose.clicked.connect(self.get_txtfile)

        self.btn_dwnld_files = QPushButton('Выбрать папку для сохранения', self)
        self.btn_dwnld_files.move(50, 150)
        self.btn_dwnld_files.clicked.connect(self.get_filepath)
        self.btn_wget = QPushButton('Начать загрузку', self)
        self.btn_wget.clicked.connect(self.start_download)
        self.btn_wget.move(50, 180)

        self.filedialog = QFileDialog()
        self.setGeometry(0, 0, 350, 250)
        self.setWindowTitle('ПРОГРАММА ДЛЯ СКАЧИВАНИЯ ПРОФИЛЕЙ')
        self.show()

    def get_txtfile(self):
        self.filepath = QFileDialog.getOpenFileName()
        self.cmd1 = 'wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --auth-no-challenge=on --keep-session-cookies --content-disposition -i '
        print(self.filepath)

    def get_filepath(self):
        self.filepath_destination = QFileDialog.getExistingDirectory()
        print(self.filepath_destination)

    def start_download(self):
        os.system('wget --directory-prefix=' + self.filepath_destination[2:] + ' --load-cookies C:\.urs_cookies --save-cookies C:\.urs_cookies --auth-no-challenge=on --keep-session-cookies --user='+self.text_login.text()+' --password='+self.text_pass.text()+' --content-disposition -i '+self.filepath[0])

    def location_on_the_screen(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()
        x = round(ag.width()/3)
        y = round(ag.height()/3)
        self.move(x, y)

if __name__.endswith('__main__'):
    app = QApplication(sys.argv)
    ex = Window()
    ex.location_on_the_screen()
    sys.exit(app.exec_())
