# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_scenario_properties.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogScenarioProperties(object):
    def setupUi(self, DialogScenarioProperties):
        if not DialogScenarioProperties.objectName():
            DialogScenarioProperties.setObjectName(u"DialogScenarioProperties")
        DialogScenarioProperties.resize(481, 395)
        self.verticalLayout_3 = QVBoxLayout(DialogScenarioProperties)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.groupBoxSimulation = QGroupBox(DialogScenarioProperties)
        self.groupBoxSimulation.setObjectName(u"groupBoxSimulation")
        self.groupBoxSimulation.setMinimumSize(QSize(250, 0))
        self.verticalLayout = QVBoxLayout(self.groupBoxSimulation)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBoxSimulation)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(80, 0))

        self.horizontalLayout.addWidget(self.label)

        self.lineEditStartTime = QLineEdit(self.groupBoxSimulation)
        self.lineEditStartTime.setObjectName(u"lineEditStartTime")
        self.lineEditStartTime.setMinimumSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.lineEditStartTime)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.groupBoxSimulation)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEditStopTime = QLineEdit(self.groupBoxSimulation)
        self.lineEditStopTime.setObjectName(u"lineEditStopTime")
        self.lineEditStopTime.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_2.addWidget(self.lineEditStopTime)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.groupBoxSimulation)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_3.addWidget(self.label_3)

        self.lineEditRandomSeed = QLineEdit(self.groupBoxSimulation)
        self.lineEditRandomSeed.setObjectName(u"lineEditRandomSeed")

        self.horizontalLayout_3.addWidget(self.lineEditRandomSeed)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6.addWidget(self.groupBoxSimulation)

        self.groupBoxOutput = QGroupBox(DialogScenarioProperties)
        self.groupBoxOutput.setObjectName(u"groupBoxOutput")
        self.groupBoxOutput.setMinimumSize(QSize(200, 0))
        self.verticalLayout_2 = QVBoxLayout(self.groupBoxOutput)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.groupBoxOutput)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.spinBoxInterval = QSpinBox(self.groupBoxOutput)
        self.spinBoxInterval.setObjectName(u"spinBoxInterval")

        self.horizontalLayout_4.addWidget(self.spinBoxInterval)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.groupBoxOutput)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.spinBoxProcess = QSpinBox(self.groupBoxOutput)
        self.spinBoxProcess.setObjectName(u"spinBoxProcess")

        self.horizontalLayout_5.addWidget(self.spinBoxProcess)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6.addWidget(self.groupBoxOutput)

        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.groupBoxOutputFile = QGroupBox(DialogScenarioProperties)
        self.groupBoxOutputFile.setObjectName(u"groupBoxOutputFile")
        self.groupBoxOutputFile.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_7 = QHBoxLayout(self.groupBoxOutputFile)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_6 = QLabel(self.groupBoxOutputFile)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_7.addWidget(self.label_6)

        self.lineEditOutputPath = QLineEdit(self.groupBoxOutputFile)
        self.lineEditOutputPath.setObjectName(u"lineEditOutputPath")

        self.horizontalLayout_7.addWidget(self.lineEditOutputPath)

        self.buttonOutputPath = QPushButton(self.groupBoxOutputFile)
        self.buttonOutputPath.setObjectName(u"buttonOutputPath")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.buttonOutputPath.sizePolicy().hasHeightForWidth()
        )
        self.buttonOutputPath.setSizePolicy(sizePolicy)
        self.buttonOutputPath.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_7.addWidget(self.buttonOutputPath)

        self.verticalLayout_3.addWidget(self.groupBoxOutputFile)

        self.verticalSpacer = QSpacerItem(
            20, 8, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.groupBoxSchema = QGroupBox(DialogScenarioProperties)
        self.groupBoxSchema.setObjectName(u"groupBoxSchema")
        self.horizontalLayout_8 = QHBoxLayout(self.groupBoxSchema)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.comboBoxSchema = QComboBox(self.groupBoxSchema)
        self.comboBoxSchema.setObjectName(u"comboBoxSchema")

        self.horizontalLayout_8.addWidget(self.comboBoxSchema)

        self.verticalLayout_3.addWidget(self.groupBoxSchema)

        self.buttonBox = QDialogButtonBox(DialogScenarioProperties)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(DialogScenarioProperties)
        self.buttonBox.accepted.connect(DialogScenarioProperties.accept)
        self.buttonBox.rejected.connect(DialogScenarioProperties.reject)

        QMetaObject.connectSlotsByName(DialogScenarioProperties)

    # setupUi

    def retranslateUi(self, DialogScenarioProperties):
        self.groupBoxSimulation.setTitle(
            QCoreApplication.translate("DialogScenarioProperties", u"Simulation", None)
        )
        self.label.setText(
            QCoreApplication.translate("DialogScenarioProperties", u"Start time:", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("DialogScenarioProperties", u"Stop time:", None)
        )
        self.label_3.setText(
            QCoreApplication.translate(
                "DialogScenarioProperties", u"Random seed:", None
            )
        )
        self.groupBoxOutput.setTitle(
            QCoreApplication.translate("DialogScenarioProperties", u"Output", None)
        )
        self.label_4.setText(
            QCoreApplication.translate("DialogScenarioProperties", u"Interval:", None)
        )
        self.label_5.setText(
            QCoreApplication.translate("DialogScenarioProperties", u"Process:", None)
        )
        self.groupBoxOutputFile.setTitle(
            QCoreApplication.translate("DialogScenarioProperties", u"Output file", None)
        )
        self.label_6.setText(
            QCoreApplication.translate(
                "DialogScenarioProperties", u"Protobuf output file:", None
            )
        )
        self.buttonOutputPath.setText(
            QCoreApplication.translate("DialogScenarioProperties", u"...", None)
        )
        self.groupBoxSchema.setTitle(
            QCoreApplication.translate("DialogScenarioProperties", u"Schema file", None)
        )
        pass

    # retranslateUi
