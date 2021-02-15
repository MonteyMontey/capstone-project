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
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GUI.sizePolicy().hasHeightForWidth())
        GUI.setSizePolicy(sizePolicy)
        GUI.setMinimumSize(QSize(800, 600))
        GUI.setMaximumSize(QSize(800, 600))
        self.centralwidget = QWidget(GUI)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
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


        self.verticalLayout.addLayout(self.configFormLayout)

        self.envStackedWidget = QStackedWidget(self.configGroupBox)
        self.envStackedWidget.setObjectName(u"envStackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.formLayout = QFormLayout(self.page)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.gridSizeComboBox = QComboBox(self.page)
        self.gridSizeComboBox.addItem("")
        self.gridSizeComboBox.addItem("")
        self.gridSizeComboBox.addItem("")
        self.gridSizeComboBox.addItem("")
        self.gridSizeComboBox.setObjectName(u"gridSizeComboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.gridSizeComboBox)

        self.label_4 = QLabel(self.page)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.snakeVisionComboBox = QComboBox(self.page)
        self.snakeVisionComboBox.addItem("")
        self.snakeVisionComboBox.addItem("")
        self.snakeVisionComboBox.addItem("")
        self.snakeVisionComboBox.addItem("")
        self.snakeVisionComboBox.addItem("")
        self.snakeVisionComboBox.setObjectName(u"snakeVisionComboBox")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.snakeVisionComboBox)

        self.envStackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.formLayout_4 = QFormLayout(self.page_2)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.label_3 = QLabel(self.page_2)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.spinBox_2 = QSpinBox(self.page_2)
        self.spinBox_2.setObjectName(u"spinBox_2")

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.spinBox_2)

        self.envStackedWidget.addWidget(self.page_2)

        self.verticalLayout.addWidget(self.envStackedWidget)

        self.line = QFrame(self.configGroupBox)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.algLabel = QLabel(self.configGroupBox)
        self.algLabel.setObjectName(u"algLabel")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.algLabel)

        self.algComboBox = QComboBox(self.configGroupBox)
        self.algComboBox.addItem("")
        self.algComboBox.addItem("")
        self.algComboBox.addItem("")
        self.algComboBox.addItem("")
        self.algComboBox.setObjectName(u"algComboBox")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.algComboBox)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.algStackedWidget = QStackedWidget(self.configGroupBox)
        self.algStackedWidget.setObjectName(u"algStackedWidget")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.algStackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.formLayout_3 = QFormLayout(self.page_4)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_2 = QLabel(self.page_4)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.learningRateDoubleSpinBox = QDoubleSpinBox(self.page_4)
        self.learningRateDoubleSpinBox.setObjectName(u"learningRateDoubleSpinBox")
        self.learningRateDoubleSpinBox.setDecimals(4)
        self.learningRateDoubleSpinBox.setMinimum(0.000100000000000)
        self.learningRateDoubleSpinBox.setMaximum(1.000000000000000)
        self.learningRateDoubleSpinBox.setSingleStep(0.000100000000000)
        self.learningRateDoubleSpinBox.setValue(0.001000000000000)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.learningRateDoubleSpinBox)

        self.label_5 = QLabel(self.page_4)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_5)

        self.gammaDoubleSpinBox = QDoubleSpinBox(self.page_4)
        self.gammaDoubleSpinBox.setObjectName(u"gammaDoubleSpinBox")
        self.gammaDoubleSpinBox.setDecimals(4)
        self.gammaDoubleSpinBox.setMinimum(0.900000000000000)
        self.gammaDoubleSpinBox.setMaximum(1.000000000000000)
        self.gammaDoubleSpinBox.setSingleStep(0.001000000000000)
        self.gammaDoubleSpinBox.setValue(0.990000000000000)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.gammaDoubleSpinBox)

        self.label_6 = QLabel(self.page_4)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.label_6)

        self.batchSizeSpinBox = QSpinBox(self.page_4)
        self.batchSizeSpinBox.setObjectName(u"batchSizeSpinBox")
        self.batchSizeSpinBox.setMinimum(1)
        self.batchSizeSpinBox.setMaximum(256)
        self.batchSizeSpinBox.setValue(32)

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.batchSizeSpinBox)

        self.label_9 = QLabel(self.page_4)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.label_9)

        self.epsilonDoubleSpinBox = QDoubleSpinBox(self.page_4)
        self.epsilonDoubleSpinBox.setObjectName(u"epsilonDoubleSpinBox")
        self.epsilonDoubleSpinBox.setMaximum(1.000000000000000)
        self.epsilonDoubleSpinBox.setSingleStep(0.010000000000000)
        self.epsilonDoubleSpinBox.setValue(1.000000000000000)

        self.formLayout_3.setWidget(3, QFormLayout.FieldRole, self.epsilonDoubleSpinBox)

        self.label_8 = QLabel(self.page_4)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_3.setWidget(4, QFormLayout.LabelRole, self.label_8)

        self.epsilonDecDoubleSpinBox = QDoubleSpinBox(self.page_4)
        self.epsilonDecDoubleSpinBox.setObjectName(u"epsilonDecDoubleSpinBox")
        self.epsilonDecDoubleSpinBox.setDecimals(6)
        self.epsilonDecDoubleSpinBox.setMaximum(1.000000000000000)
        self.epsilonDecDoubleSpinBox.setSingleStep(0.000001000000000)
        self.epsilonDecDoubleSpinBox.setValue(0.000001000000000)

        self.formLayout_3.setWidget(4, QFormLayout.FieldRole, self.epsilonDecDoubleSpinBox)

        self.label_7 = QLabel(self.page_4)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_3.setWidget(5, QFormLayout.LabelRole, self.label_7)

        self.epsilonMinSpinBox = QDoubleSpinBox(self.page_4)
        self.epsilonMinSpinBox.setObjectName(u"epsilonMinSpinBox")
        self.epsilonMinSpinBox.setMaximum(1.000000000000000)
        self.epsilonMinSpinBox.setSingleStep(0.001000000000000)
        self.epsilonMinSpinBox.setValue(0.010000000000000)

        self.formLayout_3.setWidget(5, QFormLayout.FieldRole, self.epsilonMinSpinBox)

        self.label_10 = QLabel(self.page_4)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_3.setWidget(6, QFormLayout.LabelRole, self.label_10)

        self.layer1SpinBox = QSpinBox(self.page_4)
        self.layer1SpinBox.setObjectName(u"layer1SpinBox")
        self.layer1SpinBox.setMinimum(1)
        self.layer1SpinBox.setMaximum(1024)
        self.layer1SpinBox.setValue(64)

        self.formLayout_3.setWidget(6, QFormLayout.FieldRole, self.layer1SpinBox)

        self.label_11 = QLabel(self.page_4)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_3.setWidget(7, QFormLayout.LabelRole, self.label_11)

        self.layer2SpinBox = QSpinBox(self.page_4)
        self.layer2SpinBox.setObjectName(u"layer2SpinBox")
        self.layer2SpinBox.setMinimum(1)
        self.layer2SpinBox.setMaximum(1024)
        self.layer2SpinBox.setValue(32)

        self.formLayout_3.setWidget(7, QFormLayout.FieldRole, self.layer2SpinBox)

        self.algStackedWidget.addWidget(self.page_4)

        self.verticalLayout.addWidget(self.algStackedWidget)

        self.buttonsHorizontalLayout = QHBoxLayout()
        self.buttonsHorizontalLayout.setObjectName(u"buttonsHorizontalLayout")
        self.startButton = QPushButton(self.configGroupBox)
        self.startButton.setObjectName(u"startButton")

        self.buttonsHorizontalLayout.addWidget(self.startButton)

        self.pauseButton = QPushButton(self.configGroupBox)
        self.pauseButton.setObjectName(u"pauseButton")

        self.buttonsHorizontalLayout.addWidget(self.pauseButton)

        self.stopButton = QPushButton(self.configGroupBox)
        self.stopButton.setObjectName(u"stopButton")

        self.buttonsHorizontalLayout.addWidget(self.stopButton)


        self.verticalLayout.addLayout(self.buttonsHorizontalLayout)


        self.leftVerticalLayout.addWidget(self.configGroupBox)


        self.gridLayout_4.addLayout(self.leftVerticalLayout, 0, 0, 1, 1)

        self.gridLayout_4.setRowStretch(0, 6)
        self.gridLayout_4.setColumnStretch(0, 3)
        self.gridLayout_4.setColumnStretch(1, 4)
        GUI.setCentralWidget(self.centralwidget)
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

        self.envStackedWidget.setCurrentIndex(0)
        self.gridSizeComboBox.setCurrentIndex(1)
        self.snakeVisionComboBox.setCurrentIndex(1)
        self.algStackedWidget.setCurrentIndex(1)


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

        self.label.setText(QCoreApplication.translate("GUI", u"Grid Size: ", None))
        self.gridSizeComboBox.setItemText(0, QCoreApplication.translate("GUI", u"3x3", None))
        self.gridSizeComboBox.setItemText(1, QCoreApplication.translate("GUI", u"5x5", None))
        self.gridSizeComboBox.setItemText(2, QCoreApplication.translate("GUI", u"7x7", None))
        self.gridSizeComboBox.setItemText(3, QCoreApplication.translate("GUI", u"9x9", None))

        self.label_4.setText(QCoreApplication.translate("GUI", u"Snake Vision: ", None))
        self.snakeVisionComboBox.setItemText(0, QCoreApplication.translate("GUI", u"1", None))
        self.snakeVisionComboBox.setItemText(1, QCoreApplication.translate("GUI", u"2", None))
        self.snakeVisionComboBox.setItemText(2, QCoreApplication.translate("GUI", u"3", None))
        self.snakeVisionComboBox.setItemText(3, QCoreApplication.translate("GUI", u"4", None))
        self.snakeVisionComboBox.setItemText(4, QCoreApplication.translate("GUI", u"5", None))

        self.label_3.setText(QCoreApplication.translate("GUI", u"Paddle Size: ", None))
        self.algLabel.setText(QCoreApplication.translate("GUI", u"RL-Algorithm: ", None))
        self.algComboBox.setItemText(0, QCoreApplication.translate("GUI", u"DQN", None))
        self.algComboBox.setItemText(1, QCoreApplication.translate("GUI", u"DDDQN", None))
        self.algComboBox.setItemText(2, QCoreApplication.translate("GUI", u"DDPG", None))
        self.algComboBox.setItemText(3, QCoreApplication.translate("GUI", u"SAC", None))

        self.label_2.setText(QCoreApplication.translate("GUI", u"Learning Rate: ", None))
        self.label_5.setText(QCoreApplication.translate("GUI", u"Gamma: ", None))
        self.label_6.setText(QCoreApplication.translate("GUI", u"Batch Size: ", None))
        self.label_9.setText(QCoreApplication.translate("GUI", u"Epsilon Start:", None))
        self.label_8.setText(QCoreApplication.translate("GUI", u"Epsilon Decrease: ", None))
        self.label_7.setText(QCoreApplication.translate("GUI", u"Epsilon Min: ", None))
        self.label_10.setText(QCoreApplication.translate("GUI", u"Layer 1 Neurons: ", None))
        self.label_11.setText(QCoreApplication.translate("GUI", u"Layer 2 Neurons: ", None))
        self.startButton.setText(QCoreApplication.translate("GUI", u"Start", None))
        self.pauseButton.setText(QCoreApplication.translate("GUI", u"Pause", None))
        self.stopButton.setText(QCoreApplication.translate("GUI", u"Stop", None))
        self.menuFile.setTitle(QCoreApplication.translate("GUI", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("GUI", u"Edit", None))
        self.menuAbout.setTitle(QCoreApplication.translate("GUI", u"Documentation", None))
    # retranslateUi

