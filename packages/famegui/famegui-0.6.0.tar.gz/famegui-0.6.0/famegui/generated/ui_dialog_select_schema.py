# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_select_schema.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogSelectSchemas(object):
    def setupUi(self, DialogSelectSchemas):
        if not DialogSelectSchemas.objectName():
            DialogSelectSchemas.setObjectName(u"DialogSelectSchemas")
        DialogSelectSchemas.resize(393, 102)
        self.verticalLayout = QVBoxLayout(DialogSelectSchemas)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(DialogSelectSchemas)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.comboBoxSchemas = QComboBox(DialogSelectSchemas)
        self.comboBoxSchemas.setObjectName(u"comboBoxSchemas")
        self.comboBoxSchemas.setMinimumSize(QSize(260, 0))

        self.horizontalLayout.addWidget(self.comboBoxSchemas)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(DialogSelectSchemas)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogSelectSchemas)
        self.buttonBox.accepted.connect(DialogSelectSchemas.accept)
        self.buttonBox.rejected.connect(DialogSelectSchemas.reject)

        QMetaObject.connectSlotsByName(DialogSelectSchemas)

    # setupUi

    def retranslateUi(self, DialogSelectSchemas):
        self.label.setText(
            QCoreApplication.translate("DialogSelectSchemas", u"Schema name :", None)
        )
        pass

    # retranslateUi
