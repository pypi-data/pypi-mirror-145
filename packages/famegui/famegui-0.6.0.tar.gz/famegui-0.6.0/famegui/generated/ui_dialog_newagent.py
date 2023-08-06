# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_newagent.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogNewAgent(object):
    def setupUi(self, DialogNewAgent):
        if not DialogNewAgent.objectName():
            DialogNewAgent.setObjectName(u"DialogNewAgent")
        DialogNewAgent.resize(668, 455)
        DialogNewAgent.setMinimumSize(QSize(300, 350))
        self.verticalLayout = QVBoxLayout(DialogNewAgent)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(DialogNewAgent)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.comboBoxType = QComboBox(DialogNewAgent)
        self.comboBoxType.setObjectName(u"comboBoxType")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxType.sizePolicy().hasHeightForWidth())
        self.comboBoxType.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.comboBoxType)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.treeWidget = QTreeWidget(DialogNewAgent)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1")
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")

        self.verticalLayout.addWidget(self.treeWidget)

        self.buttonBox = QDialogButtonBox(DialogNewAgent)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogNewAgent)
        self.buttonBox.accepted.connect(DialogNewAgent.accept)
        self.buttonBox.rejected.connect(DialogNewAgent.reject)

        QMetaObject.connectSlotsByName(DialogNewAgent)

    # setupUi

    def retranslateUi(self, DialogNewAgent):
        DialogNewAgent.setWindowTitle(
            QCoreApplication.translate("DialogNewAgent", u"Dialog", None)
        )
        self.label.setText(
            QCoreApplication.translate("DialogNewAgent", u"New agent type :", None)
        )

    # retranslateUi
