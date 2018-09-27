from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QScrollArea, QHBoxLayout, QTabWidget, QLabel, QLineEdit, QGridLayout, QPushButton,
                             QMenu, QAction, QCheckBox, QVBoxLayout, QWidget, QDialog, QFrame, QTableWidgetItem,
                             QAbstractItemView, QMessageBox, QTextEdit, QHeaderView, QTableWidget, QRadioButton,
                             QFileDialog, QListWidget, QListWidgetItem)
from PyQt5.QtGui import QCursor, QFont, QFontDatabase, QPainter, QColor, QPen, QPixmap

from cpchain.crypto import ECCipher, RSACipher, Encoder

from cpchain.wallet.pages import load_stylesheet, HorizontalLine, wallet, main_wnd, get_pixm

from twisted.internet.defer import inlineCallbacks
from twisted.internet.threads import deferToThread
from cpchain.wallet import fs
from cpchain.utils import open_file, sizeof_fmt
from cpchain.proxy.client import pick_proxy

import importlib
import os
import os.path as osp
import string
import logging
import sip

from cpchain import config, root_dir
from cpchain.wallet.pages.personal import Seller

from cpchain.wallet.pages.product import Product2, TableWidget

from cpchain.wallet.pages import main_wnd
from cpchain.wallet.pages.other import PublishDialog
from cpchain.wallet.components.product import Product

from datetime import datetime as dt

class ProductList(QScrollArea):

    change = QtCore.pyqtSignal(list, name="modelChanged")

    def __init__(self, products, col=3):
        self.col = col
        super().__init__()
        self.change.connect(self.modelChanged)
        self.setProducts(products)

    def setProducts(self, products):
        products.setView(self)
        self._setProducts(products.value)

    def _setProducts(self, products):
        arr = []
        for p in products:
            item = Product(**p)
            arr.append(item)
        self.products = arr
        self.initUI()

    def modelChanged(self, value):
        layout = self.layout()
        if layout:
            QWidget().setLayout(self.layout())
        arr = []
        for p in value:
            item = Product(**p)
            arr.append(item)
        self.products = arr
        self.exec_(self.layout())

    def initUI(self):
        self.exec_(None)

    def exec_(self, layout=None):
        pds = self.products
        if len(self.products) == 0:
            return
        row = int((len(pds) + self.col / 2) / self.col + 0.5)
        if not layout:
            layout = QGridLayout()
            widget = QWidget()
            widget.setObjectName('parent_widget')
            widget.setLayout(layout)
            widget.setFixedWidth(720)
            widget.setFixedHeight(250 * row)
            widget.setStyleSheet("QWidget#parent_widget{background: transparent;}")

            # Scroll Area Properties
            scroll = QScrollArea()
            scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll.setWidgetResizable(True)
            # scroll.setFixedHeight(800)
            scroll.setWidget(widget)

            self.setWidget(scroll)
            self.setWidgetResizable(True)

        layout.setAlignment(Qt.AlignTop)
        for i in range(row):
            for j in range(self.col):
                index = i * self.col + j
                if index < len(pds):
                    layout.addWidget(pds[index], i, j)
                else:
                    tmp = QLabel('')
                    layout.addWidget(tmp, i, j)
        self.setObjectName('main')
        self.setStyleSheet("""
            #main_layout {
                height: 800px;
            }
        """)