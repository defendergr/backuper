#Backuper έκδοση 1.2.0 Κωνσταντίνος Καρακασίδης

from dirsync import sync
import configparser
import os
from datetime import datetime

import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QThread, Signal, QFile, Qt, QProcess
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox, QTextBrowser
from PySide6.QtGui import QIcon, QTextCursor

class Synchronize():
    # #TODO neo class gia thread worker
    # def __int__(self):
    #     pass
    def sync(self):
        # self.startButton.setEnabled(False)
        if os.path.isfile(self.paths):
            config = configparser.ConfigParser()
            config.read(self.paths)
            source_path = config.get('DEFAULT','source')
            target_path = config.get('DEFAULT','target')

            option = 'sync'

            sync(r'{}'.format(source_path), r'{}'.format(target_path), option, verbose=True, purge=True) #for syncing one way + purge
            self.out()

        else:
            print(f'Δεν βρέθηκε το {self.paths}')


    def out(self):
        with open(self.date + '_log.txt', 'r', encoding='utf-8') as output:
            out = output.read()
            self.output.setText(out)
            self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())
        # self.startButton.setEnabled(True)




class MainWindow(Synchronize):

    def __init__(self):
        self.process = QProcess()
        self.date = datetime.now().strftime('%d-%m-%Y')
        sys.stdout = open(self.date + '_log.txt', 'w', encoding='utf-8')

        super(MainWindow, self).__init__()
        app = QApplication(sys.argv)
        app.setStyleSheet(
            'QMainWindow{background-color: darkgray;} '
            'QTextBrowser{background-color: black; color: lightgreen;}'
            'QPushButton{border-radius: 5px; background-color: lightgray;}'
                          )
        ui_file_name = "form.ui"
        ui_file = QFile(ui_file_name)
        loader = QUiLoader()
        window = loader.load(ui_file)
        ui_file.close()

        # this keep window top
        # window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        # window title
        window.setWindowTitle('Backuper έκδοση 1.2.0')

        # window icon
        window.setWindowIcon(QIcon('dimos.ico'))

        # # this will hide the title bar
        # window.setWindowFlag(Qt.FramelessWindowHint)

        self.paths = 'options.cfg'
        if os.path.isfile(self.paths):
            self.config = configparser.ConfigParser()
            self.config.read(self.paths)
            self.source_path = self.config.get('DEFAULT', 'source')
            self.target_path = self.config.get('DEFAULT', 'target')

        window.SourceButton.clicked.connect(lambda: self.fileBrowser('source'))
        window.TargetButton.clicked.connect(lambda: self.fileBrowser('target'))

        window.StopButton.clicked.connect(self.stop)


        self.output = window.Output


        self.sourceLine = window.SourceLine
        self.sourceLine.setText(self.source_path)
        self.targetLine = window.TargetLine
        self.targetLine.setText(self.target_path)

        self.startButton = window.StartButton
        self.startButton.clicked.connect(self.callSync)

        # self.process.started(lambda: self.startButton.setEnabled(False))
        # self.process.finished(lambda: self.startButton.setEnabled(True))


        window.InfoButton.clicked.connect(self.about)

        window.show()
        app.exec()

    def fileBrowser(self, pos):
        self.dialog = QFileDialog()

        if pos == 'source':
            directory = self.dialog.getExistingDirectoryUrl().path()[1:]
            print(directory)
            self.sourceLine.setText(directory)
            self.config['DEFAULT']['source'] = directory
        elif pos == 'target':
            directory = self.dialog.getExistingDirectoryUrl().path()[1:]
            print(directory)
            self.targetLine.setText(directory)
            self.config['DEFAULT']['target'] = directory

        with open(self.paths, 'w') as configfile:
            self.config.write(configfile)
        self.paths = 'options.cfg'


    def stop(self):
        sys.exit()

    def about(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('About')
        msgBox.setWindowIcon(QIcon('dimos.ico'))
        msgBox.setText("Backuper έκδοση 1.2.0 \nΓια τον Δήμο Θέρμης \nΚωνσταντίνος Καρακασίδης")
        msgBox.exec()

    def callSync(self):
        # run the process
        # `start` takes the exec and a list of arguments
        self.process.start(self.sync())

if __name__=="__main__":
    MainWindow()
