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
        GUI.setEnabled(True)
        GUI.resize(800, 600)
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
        self.envGroupBox = QGroupBox(self.centralwidget)
        self.envGroupBox.setObjectName(u"envGroupBox")
        self.envGroupBox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.envGroupBox.setFlat(False)
        self.envGroupBox.setCheckable(False)
        self.envGroupBox.setChecked(False)
        self.verticalLayout_2 = QVBoxLayout(self.envGroupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.envView = QGraphicsView(self.envGroupBox)
        self.envView.setObjectName(u"envView")
        self.envView.setFrameShape(QFrame.StyledPanel)
        self.envView.setFrameShadow(QFrame.Sunken)
        self.envView.setLineWidth(1)
        self.envView.setMidLineWidth(0)

        self.verticalLayout_2.addWidget(self.envView)


        self.rightVerticalLayout.addWidget(self.envGroupBox)

        self.learningGraphGroupBox = QGroupBox(self.centralwidget)
        self.learningGraphGroupBox.setObjectName(u"learningGraphGroupBox")
        self.verticalLayout_3 = QVBoxLayout(self.learningGraphGroupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.learningGraphView = QGraphicsView(self.learningGraphGroupBox)
        self.learningGraphView.setObjectName(u"learningGraphView")
        self.learningGraphView.setFrameShape(QFrame.StyledPanel)

        self.verticalLayout_3.addWidget(self.learningGraphView)


        self.rightVerticalLayout.addWidget(self.learningGraphGroupBox)


        self.gridLayout_4.addLayout(self.rightVerticalLayout, 0, 1, 1, 1)

        self.leftVerticalLayout = QVBoxLayout()
        self.leftVerticalLayout.setObjectName(u"leftVerticalLayout")
        self.leftVerticalLayout.setContentsMargins(-1, 0, -1, -1)
        self.configGroupBox = QGroupBox(self.centralwidget)
        self.configGroupBox.setObjectName(u"configGroupBox")
        self.verticalLayout = QVBoxLayout(self.configGroupBox)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.configFormLayout = QFormLayout()
        self.configFormLayout.setObjectName(u"configFormLayout")
        self.configFormLayout.setVerticalSpacing(10)
        self.configFormLayout.setContentsMargins(-1, 0, 0, -1)
        self.envLabel = QLabel(self.configGroupBox)
        self.envLabel.setObjectName(u"envLabel")

        self.configFormLayout.setWidget(0, QFormLayout.LabelRole, self.envLabel)

        self.envComboBox = QComboBox(self.configGroupBox)
        self.envComboBox.addItem("")
        self.envComboBox.addItem("")
        self.envComboBox.addItem("")
        self.envComboBox.setObjectName(u"envComboBox")

        self.configFormLayout.setWidget(0, QFormLayout.FieldRole, self.envComboBox)

        self.algLabel = QLabel(self.configGroupBox)
        self.algLabel.setObjectName(u"algLabel")

        self.configFormLayout.setWidget(1, QFormLayout.LabelRole, self.algLabel)

        self.algComboBox = QComboBox(self.configGroupBox)
        self.algComboBox.addItem("")
        self.algComboBox.addItem("")
        self.algComboBox.addItem("")
        self.algComboBox.addItem("")
        self.algComboBox.setObjectName(u"algComboBox")

        self.configFormLayout.setWidget(1, QFormLayout.FieldRole, self.algComboBox)


        self.verticalLayout.addLayout(self.configFormLayout)

        self.buttonsHorizontalLayout = QHBoxLayout()
        self.buttonsHorizontalLayout.setObjectName(u"buttonsHorizontalLayout")
        self.stopButton = QPushButton(self.configGroupBox)
        self.stopButton.setObjectName(u"stopButton")

        self.buttonsHorizontalLayout.addWidget(self.stopButton)

        self.pauseButton = QPushButton(self.configGroupBox)
        self.pauseButton.setObjectName(u"pauseButton")

        self.buttonsHorizontalLayout.addWidget(self.pauseButton)

        self.startButton = QPushButton(self.configGroupBox)
        self.startButton.setObjectName(u"startButton")

        self.buttonsHorizontalLayout.addWidget(self.startButton)


        self.verticalLayout.addLayout(self.buttonsHorizontalLayout)


        self.leftVerticalLayout.addWidget(self.configGroupBox)


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
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
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
        self.envComboBox.activated.connect(self.learningGraphGroupBox.repaint)

        QMetaObject.connectSlotsByName(GUI)
    # setupUi

    def retranslateUi(self, GUI):
        GUI.setWindowTitle(QCoreApplication.translate("GUI", u"Capstone Project", None))
        self.envGroupBox.setTitle(QCoreApplication.translate("GUI", u"Environment", None))
        self.learningGraphGroupBox.setTitle(QCoreApplication.translate("GUI", u"Learning Graph", None))
        self.configGroupBox.setTitle(QCoreApplication.translate("GUI", u"Configuration", None))
        self.envLabel.setText(QCoreApplication.translate("GUI", u"Environment: ", None))
        self.envComboBox.setItemText(0, QCoreApplication.translate("GUI", u"Snake", None))
        self.envComboBox.setItemText(1, QCoreApplication.translate("GUI", u"Breakout", None))
        self.envComboBox.setItemText(2, QCoreApplication.translate("GUI", u"Pong", None))

        self.algLabel.setText(QCoreApplication.translate("GUI", u"RL-Algorithm: ", None))
        self.algComboBox.setItemText(0, QCoreApplication.translate("GUI", u"DQN", None))
        self.algComboBox.setItemText(1, QCoreApplication.translate("GUI", u"DDDQN", None))
        self.algComboBox.setItemText(2, QCoreApplication.translate("GUI", u"DDPG", None))
        self.algComboBox.setItemText(3, QCoreApplication.translate("GUI", u"SAC", None))

        self.stopButton.setText(QCoreApplication.translate("GUI", u"Start", None))
        self.pauseButton.setText(QCoreApplication.translate("GUI", u"Pause", None))
        self.startButton.setText(QCoreApplication.translate("GUI", u"Stop", None))
        self.menuFile.setTitle(QCoreApplication.translate("GUI", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("GUI", u"Edit", None))
        self.menuAbout.setTitle(QCoreApplication.translate("GUI", u"Documentation", None))
    # retranslateUi

