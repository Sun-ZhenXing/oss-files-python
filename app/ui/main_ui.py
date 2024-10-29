# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLineEdit,
    QMenu,
    QMenuBar,
    QPushButton,
    QSplitter,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from app.components.DragDropTreeView import DragDropTreeView


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.action_S = QAction(MainWindow)
        self.action_S.setObjectName("action_S")
        self.action_X = QAction(MainWindow)
        self.action_X.setObjectName("action_X")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName("splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.gridLayoutWidget = QWidget(self.splitter)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.gridLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.reloadPushButton = QPushButton(self.gridLayoutWidget)
        self.reloadPushButton.setObjectName("reloadPushButton")

        self.horizontalLayout_2.addWidget(self.reloadPushButton)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.remoteTreeView = DragDropTreeView(self.gridLayoutWidget)
        self.remoteTreeView.setObjectName("remoteTreeView")

        self.verticalLayout.addWidget(self.remoteTreeView)

        self.splitter.addWidget(self.gridLayoutWidget)
        self.gridLayoutWidget_2 = QWidget(self.splitter)
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.verticalLayout_2 = QVBoxLayout(self.gridLayoutWidget_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.rootDirLineEdit = QLineEdit(self.gridLayoutWidget_2)
        self.rootDirLineEdit.setObjectName("rootDirLineEdit")

        self.horizontalLayout_3.addWidget(self.rootDirLineEdit)

        self.rootDirPushButton = QPushButton(self.gridLayoutWidget_2)
        self.rootDirPushButton.setObjectName("rootDirPushButton")

        self.horizontalLayout_3.addWidget(self.rootDirPushButton)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.localTreeView = DragDropTreeView(self.gridLayoutWidget_2)
        self.localTreeView.setObjectName("localTreeView")

        self.verticalLayout_2.addWidget(self.localTreeView)

        self.splitter.addWidget(self.gridLayoutWidget_2)

        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        self.menu_F = QMenu(self.menubar)
        self.menu_F.setObjectName("menu_F")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
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
        MainWindow.setWindowTitle(
            QCoreApplication.translate(
                "MainWindow", "OSS \u6587\u4ef6\u7ba1\u7406", None
            )
        )
        self.action_S.setText(
            QCoreApplication.translate("MainWindow", "\u8bbe\u7f6e(&S)", None)
        )
        self.action_X.setText(
            QCoreApplication.translate("MainWindow", "\u9000\u51fa(&X)", None)
        )
        self.reloadPushButton.setText(
            QCoreApplication.translate(
                "MainWindow", "\u5237\u65b0\u6587\u4ef6(&R)", None
            )
        )
        self.rootDirLineEdit.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "\u6839\u76ee\u5f55", None)
        )
        self.rootDirPushButton.setText(
            QCoreApplication.translate(
                "MainWindow", "\u9009\u62e9\u6839\u76ee\u5f55(&S)", None
            )
        )
        self.menu_F.setTitle(
            QCoreApplication.translate("MainWindow", "\u6587\u4ef6(&F)", None)
        )
        # retranslateUi

        MainWindow.setWindowTitle(
            QCoreApplication.translate(
                "MainWindow", "OSS \u6587\u4ef6\u7ba1\u7406", None
            )
        )
        self.action_S.setText(
            QCoreApplication.translate("MainWindow", "\u8bbe\u7f6e(&S)", None)
        )
        self.action_X.setText(
            QCoreApplication.translate("MainWindow", "\u9000\u51fa(&X)", None)
        )
        self.reloadPushButton.setText(
            QCoreApplication.translate(
                "MainWindow", "\u5237\u65b0\u6587\u4ef6(&R)", None
            )
        )
        self.rootDirLineEdit.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "\u6839\u76ee\u5f55", None)
        )
        self.rootDirPushButton.setText(
            QCoreApplication.translate(
                "MainWindow", "\u9009\u62e9\u6839\u76ee\u5f55(&S)", None
            )
        )
        self.menu_F.setTitle(
            QCoreApplication.translate("MainWindow", "\u6587\u4ef6(&F)", None)
        )

    # retranslateUi
