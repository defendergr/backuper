#Backuper έκδοση 1.5.3 Κωνσταντίνος Καρακασίδης

import configparser
import os
from datetime import datetime

import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QProcess
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox
from PySide6.QtGui import QIcon



class MainWindow():

    def __init__(self):
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.stdoutReady)

        self.date = datetime.now().strftime('%#d-%#m-%Y')

        super(MainWindow, self).__init__()
        app = QApplication(sys.argv)
        app.setStyleSheet(
            'QMainWindow{background-color: darkgray;} '
            'QTextBrowser{background-color: black; color: lightgreen;}'
            'QPushButton{border-radius: 5px; background-color: lightgray;}'
                          )
        app.processEvents()
        ui_file_name = "form.ui"
        ui_file = QFile(ui_file_name)
        loader = QUiLoader()
        window = loader.load(ui_file)
        ui_file.close()

        # this keep window top
        # window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        # window title
        window.setWindowTitle('Backuper έκδοση 1.5.3')

        # window icon
        window.setWindowIcon(QIcon('dimos.ico'))

        # window NO Resize
        window.setFixedSize(window.width(), window.height())

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
        self.startButton.clicked.connect(self.start)

        # self.process.started(lambda: self.startButton.setEnabled(False))
        # self.process.finished(lambda: self.startButton.setEnabled(True))


        window.InfoButton.clicked.connect(self.about)

        window.show()
        app.exec()


    def start(self):
        self.startButton.setEnabled(False)
        self.process.start('mainSync\sync.exe')


    def fileBrowser(self, pos):
        self.startButton.setEnabled(True)
        self.dialog = QFileDialog()

        if pos == 'source':
            directory = self.dialog.getExistingDirectoryUrl().path()[1:]
            if directory != '':
                print(directory)
                self.sourceLine.setText(directory)
                self.config['DEFAULT']['source'] = directory
        elif pos == 'target':
            directory = self.dialog.getExistingDirectoryUrl().path()[1:]
            if directory != '':
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
        msgBox.setText("Backuper έκδοση 1.2.0 \nΓια τον Δήμο Θέρμης \nΑπό: Κωνσταντίνος Καρακασίδης")
        msgBox.exec()

    def out(self, text):
        self.output.setText(text)
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())

    def stdoutReady(self):
        text = self.process.readAllStandardOutput()
        log = text.data().decode('windows-1253')
        with open('log/'+self.date + '_log.txt', 'a', encoding='utf-8') as l:
            l.write(log)
        self.out(str(log))


if __name__=="__main__":
    MainWindow()
