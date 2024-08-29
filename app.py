import sys
import time
import json
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QComboBox, QLabel, QMenuBar, QTextEdit, QStatusBar, QSplitter,     QSizePolicy, QTextBrowser, QStackedWidget, QHBoxLayout, QVBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QKeySequence, QTextCursor
import markdown
import httpx
from pyollama import run_model, convert_nanoseconds_to_seconds, list_models_names

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 800, 800
        self.setMinimumSize(self.window_width, self.window_height)
        self.setWindowTitle('Ollama Prompt & Response App V1')
        self.setWindowIcon(QIcon('./icons/logo.png'))
        self.setObjectName('mainwindow')
        # Qwidget:window {background-color: #1b2b39;}
        self.setStyleSheet('''
            font-size: 16px;
        ''')

        self.layout = {}
        self.layout['main'] = QVBoxLayout()
        self.setLayout(self.layout['main'])

        self.response_log = []

        self.init_ul()
    
    def init_ui(self):
        self.layout['model'] = QHBoxLayout()
        self.layout['main'].addLayout(self.layout['model'])

        label_model = QLabel('Model:')
        label_model.setFixedWidth(60)
        self.combo_box = QComboBox()
        self.combo_box.setFixedWidth(250)
        self.combo_box.addItems(models)
        self.layout['model'].addWidget(label_model)
        self.layout['model'].addWidget(self.combo_box)
        self.layout['model'].addStretch()


if __name__ == '__main__':
    try:
        models = list_models_names()
        ollama_offline = False
    except httpx.ConnectError:
        models = []
        ollama_offline = True

    app = QApplication(sys.argv)
    app.setStyleSheet(open('stylesheet.css').read())

    myApp = AppWindow()
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')