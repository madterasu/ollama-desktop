import sys
import time
import json
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QComboBox, QLabel, QMenuBar, QTextEdit, QStatusBar, QSplitter,     QSizePolicy, QTextBrowser, QStackedWidget, QHBoxLayout, QVBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QKeySequence, QTextCursor
import markdown
import httpx
from pyollama import run_model, convert_nanoseconds_to_seconds, list_models_names

