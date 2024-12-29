# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSplitter, QStatusBar,
    QVBoxLayout, QWidget)

from app.components.DragDropTreeView import DragDropTreeView

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.action_S = QAction(MainWindow)
        self.action_S.setObjectName(u"action_S")
        self.action_X = QAction(MainWindow)
        self.action_X.setObjectName(u"action_X")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.gridLayoutWidget = QWidget(self.splitter)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.gridLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.reloadPushButton = QPushButton(self.gridLayoutWidget)
        self.reloadPushButton.setObjectName(u"reloadPushButton")

        self.horizontalLayout_2.addWidget(self.reloadPushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.remoteTreeView = DragDropTreeView(self.gridLayoutWidget)
        self.remoteTreeView.setObjectName(u"remoteTreeView")

        self.verticalLayout.addWidget(self.remoteTreeView)

        self.splitter.addWidget(self.gridLayoutWidget)
        self.gridLayoutWidget_2 = QWidget(self.splitter)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.verticalLayout_2 = QVBoxLayout(self.gridLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.rootDirLineEdit = QLineEdit(self.gridLayoutWidget_2)
        self.rootDirLineEdit.setObjectName(u"rootDirLineEdit")

        self.horizontalLayout_3.addWidget(self.rootDirLineEdit)

        self.rootDirPushButton = QPushButton(self.gridLayoutWidget_2)
        self.rootDirPushButton.setObjectName(u"rootDirPushButton")

        self.horizontalLayout_3.addWidget(self.rootDirPushButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.localTreeView = DragDropTreeView(self.gridLayoutWidget_2)
        self.localTreeView.setObjectName(u"localTreeView")

        self.verticalLayout_2.addWidget(self.localTreeView)

        self.splitter.addWidget(self.gridLayoutWidget_2)

        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        self.menu_F = QMenu(self.menubar)
        self.menu_F.setObjectName(u"menu_F")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_F.menuAction())
        self.menu_F.addAction(self.action_S)
        self.menu_F.addSeparator()
        self.menu_F.addAction(self.action_X)

        self.retranslateUi(MainWindow)
        self.reloadPushButton.clicked.connect(MainWindow.reloadFiles)
        self.rootDirPushButton.clicked.connect(MainWindow.selectRoot)
        self.rootDirLineEdit.returnPressed.connect(MainWindow.changeRoot)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"OSS \u6587\u4ef6\u7ba1\u7406", None))
        self.action_S.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e(&S)", None))
        self.action_X.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa(&X)", None))
        self.reloadPushButton.setText(QCoreApplication.translate("MainWindow", u"\u5237\u65b0\u6587\u4ef6(&R)", None))
        self.rootDirLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u6839\u76ee\u5f55", None))
        self.rootDirPushButton.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6839\u76ee\u5f55(&S)", None))
        self.menu_F.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6(&F)", None))
    # retranslateUi

