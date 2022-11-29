#Backuper έκδοση 1.2.0 Κωνσταντίνος Καρακασίδης

from dirsync import sync
import configparser
import os

import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QThread, Signal, QFile, Qt
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox
from PySide6.QtGui import QIcon



class MainWindow():

    def __init__(self):
        super(MainWindow, self).__init__()
        app = QApplication(sys.argv)
        app.setStyleSheet('QMainWindow{background-color: darkgray;} '
                          'QProgressBar{border-radius: 5px; background-color: gray;} '
                          'QProgressBar::chunk {border-radius: 5px; background-color: #F433FF;}'
                          'QProgressBar{text-align:center; font:bold} '
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
        window.setWindowFlag(Qt.FramelessWindowHint)

        self.paths = 'options.cfg'
        if os.path.isfile(self.paths):
            self.config = configparser.ConfigParser()
            self.config.read(self.paths)
            self.source_path = self.config.get('DEFAULT', 'source')
            self.target_path = self.config.get('DEFAULT', 'target')

        window.SourceButton.clicked.connect(lambda: self.fileBrowser('source'))
        window.TargetButton.clicked.connect(lambda: self.fileBrowser('target'))

        window.StopButton.clicked.connect(self.stop)

        self.sourceLine = window.SourceLine
        self.sourceLine.setText(self.source_path)
        self.targetLine = window.TargetLine
        self.targetLine.setText(self.target_path)

        window.StartButton.clicked.connect(self.sync)

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

    def sync(self):
        paths = 'options.cfg'
        if os.path.isfile(paths):
            config = configparser.ConfigParser()
            config.read(paths)
            source_path = config.get('DEFAULT','source')
            target_path = config.get('DEFAULT','target')

            option = 'sync'

            sync(r'{}'.format(source_path), r'{}'.format(target_path), option, verbose=True, purge=True) #for syncing one way + purge
        else:
            print(f'Δεν βρέθηκε το {paths}')

    def stop(self):
        sys.exit()

    def about(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('About')
        msgBox.setWindowIcon(QIcon('dimos.ico'))
        msgBox.setText("Backuper έκδοση 1.2.0 \nΓια τον Δήμο Θέρμης \nΚωνσταντίνος Καρακασίδης")
        msgBox.exec()


if __name__=="__main__":
    MainWindow()