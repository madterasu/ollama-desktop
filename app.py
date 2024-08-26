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