import sys
import time
import json
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QComboBox, QLabel, QMenuBar, QTextEdit, QStatusBar, QSplitter,     QSizePolicy, QTextBrowser, QStackedWidget, QHBoxLayout, QVBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QKeySequence, QTextCursor
import markdown
import httpx
from pyollama import run_model, convert_nanoseconds_to_seconds, list_models_names

class PlainTextPasteQTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoNone)

    def keyPressEvent(self, e):
        if e.matches(QKeySequence.StandardKey.Paste):
            self.insertPlainText(QApplication.clipboard().text())
        else:
            super().keyPressEvent(e)
    
class LabeledTextEdit(QWidget):
    def __init__(self, label_text, text_edit):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(label_text))
        layout.addWidget(text_edit)

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

        self.init_ui()
    
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

        self.prompt_input = PlainTextPasteQTextEdit()
        self.prompt_input_window = LabeledTextEdit('Prompt', self.prompt_input)

        self.prompt_response = QTextBrowser()
        self.prompt_response_window = LabeledTextEdit('Response:', self.prompt_response)

        splitter = QSplitter()
        splitter.setOrientation(Qt.Orientation.Vertical)
        splitter.addWidget(self.prompt_input_window)
        splitter.addWidget(self.prompt_response_window)
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        self.layout['main'].addWidget(splitter)

        self.layout['buttons'] = QHBoxLayout()
        self.layout['main'].addLayout(self.layout['buttons'])
        self.btn_generate = QPushButton('&Generate', clicked=self.run_model)
        self.btn_generate.setFixedWidth(200)
        self.btn_clear = QPushButton('&Reset', clicked=self.reset)
        self.btn_clear.setFixedWidth(100)
        self.layout['buttons'].addStretch()
        self.layout['buttons'].addWidget(self.btn_generate)
        self.layout['buttons'].addWidget(self.btn_clear)

        self.label_copyright = QLabel("<a style='color: #79d6b5'>UMSIDA 2024</a>")
        self.label_copyright.setOpenExternalLinks(True)

        self.status_bar = QStatusBar()
        self.status_bar.addPermanentWidget(self.label_copyright)
        self.layout['main'].addWidget(self.status_bar)

        if ollama_offline:
            self.status_bar.showMessage('Ollama Offline')
        else:
            self.status_bar.showMessage('Ollama Online')

    def reset(self):
        self.prompt_input.clear()
        self.prompt_response.clear()
        self.status_bar.clear()
        self.response_log = []

    def run_model(self):
        model = self.combo_box.currentText()
        prompt = self.prompt_input.toPlainText()
        if not prompt.strip():
            self.status_bar.showMessage('Prompt is empty. Please enter a prompt.')
            return
        try:
            response = run_model(model, prompt)
        except Exception as e:
            self.status_bar.showMessage(f'Error: {e}')
            return
        
        html = markdown.markdown(response['response'].strip(), extensions=['nl2br'])
        # print(response)
        self.response_log.append(
            {
                'model': model,
                'prompt': prompt,
                'response': response['response'],
                'total_duration': convert_nanoseconds_to_seconds(response['total_duration']),
                'prompt_eval_count': response.get('prompt_eval_count', 0),
                'eval_count': response['eval_count']
            }
        )

        self.prompt_response.append(html + '\n\n')
        self.status_bar.showMessage(f'Total duration: {convert_nanoseconds_to_seconds(response["total_duration"]):.2f} seconds. Tokens (prompt)')

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