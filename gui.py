# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_GUI(object):
    def setupUi(self, GUI):
        if not GUI.objectName():
            GUI.setObjectName(u"GUI")
        GUI.resize(789, 655)
        self.centralwidget = QWidget(GUI)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_4 = QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(20)
        self.gridLayout_4.setContentsMargins(-1, -1, 9, -1)
        self.rightVerticalLayout = QVBoxLayout()
        self.rightVerticalLayout.setSpacing(6)
        self.rightVerticalLayout.setObjectName(u"rightVerticalLayout")
        self.rightVerticalLayout.setContentsMargins(-1, 0, -1, -1)
        self.learningGraphGroupBox = QGroupBox(self.centralwidget)
        self.learningGraphGroupBox.setObjectName(u"learningGraphGroupBox")
        self.learningGraphGroupBox.setCheckable(False)
        self.learningGraphGroupBox.setChecked(False)

        self.rightVerticalLayout.addWidget(self.learningGraphGroupBox)

        self.environmentGroupBox = QGroupBox(self.centralwidget)
        self.environmentGroupBox.setObjectName(u"environmentGroupBox")

        self.rightVerticalLayout.addWidget(self.environmentGroupBox)


        self.gridLayout_4.addLayout(self.rightVerticalLayout, 0, 1, 1, 1)

        self.leftVerticalLayout = QVBoxLayout()
        self.leftVerticalLayout.setObjectName(u"leftVerticalLayout")
        self.leftVerticalLayout.setContentsMargins(-1, 20, -1, -1)
        self.configFormLayout = QFormLayout()
        self.configFormLayout.setObjectName(u"configFormLayout")
        self.configFormLayout.setVerticalSpacing(10)
        self.configFormLayout.setContentsMargins(-1, 0, 0, -1)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.configFormLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.configFormLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.configFormLayout.setWidget(0, QFormLayout.FieldRole, self.comboBox)

        self.comboBox_2 = QComboBox(self.centralwidget)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.configFormLayout.setWidget(1, QFormLayout.FieldRole, self.comboBox_2)


        self.leftVerticalLayout.addLayout(self.configFormLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_3.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_3.addWidget(self.pushButton)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_3.addWidget(self.pushButton_3)


        self.leftVerticalLayout.addLayout(self.horizontalLayout_3)


        self.gridLayout_4.addLayout(self.leftVerticalLayout, 0, 0, 1, 1)

        self.gridLayout_4.setRowStretch(0, 6)
        self.gridLayout_4.setColumnStretch(0, 3)
        self.gridLayout_4.setColumnStretch(1, 4)
        GUI.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(GUI)
        self.statusbar.setObjectName(u"statusbar")
        GUI.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(GUI)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 789, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        GUI.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(GUI)

        QMetaObject.connectSlotsByName(GUI)
    # setupUi

    def retranslateUi(self, GUI):
        GUI.setWindowTitle(QCoreApplication.translate("GUI", u"Capstone Project", None))
        self.learningGraphGroupBox.setTitle(QCoreApplication.translate("GUI", u"Environment", None))
        self.environmentGroupBox.setTitle(QCoreApplication.translate("GUI", u"Learning Graph", None))
        self.label.setText(QCoreApplication.translate("GUI", u"Environment: ", None))
        self.label_2.setText(QCoreApplication.translate("GUI", u"RL-Algorithm: ", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("GUI", u"Snake", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("GUI", u"Breakout", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("GUI", u"Pong", None))

        self.comboBox_2.setItemText(0, QCoreApplication.translate("GUI", u"DQN", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("GUI", u"DDDQN", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("GUI", u"DDPG", None))
        self.comboBox_2.setItemText(3, QCoreApplication.translate("GUI", u"SAC", None))

        self.pushButton_2.setText(QCoreApplication.translate("GUI", u"Start", None))
        self.pushButton.setText(QCoreApplication.translate("GUI", u"Pause", None))
        self.pushButton_3.setText(QCoreApplication.translate("GUI", u"Stop", None))
        self.menuFile.setTitle(QCoreApplication.translate("GUI", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("GUI", u"Edit", None))
        self.menuAbout.setTitle(QCoreApplication.translate("GUI", u"Documentation", None))
    # retranslateUi

