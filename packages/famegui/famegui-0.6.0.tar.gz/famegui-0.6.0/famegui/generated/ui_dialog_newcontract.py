# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_newcontract.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogNewContract(object):
    def setupUi(self, DialogNewContract):
        if not DialogNewContract.objectName():
            DialogNewContract.setObjectName(u"DialogNewContract")
        DialogNewContract.resize(417, 226)
        self.verticalLayout = QVBoxLayout(DialogNewContract)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelDescr = QLabel(DialogNewContract)
        self.labelDescr.setObjectName(u"labelDescr")
        self.labelDescr.setWordWrap(True)

        self.verticalLayout.addWidget(self.labelDescr)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(DialogNewContract)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.comboBoxProduct = QComboBox(DialogNewContract)
        self.comboBoxProduct.setObjectName(u"comboBoxProduct")

        self.horizontalLayout.addWidget(self.comboBoxProduct)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(DialogNewContract)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.lineFirstDeliveryTime = QLineEdit(DialogNewContract)
        self.lineFirstDeliveryTime.setObjectName(u"lineFirstDeliveryTime")
        self.lineFirstDeliveryTime.setMaximumSize(QSize(160, 16777215))

        self.horizontalLayout_2.addWidget(self.lineFirstDeliveryTime)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(DialogNewContract)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.lineDeliveryInterval = QLineEdit(DialogNewContract)
        self.lineDeliveryInterval.setObjectName(u"lineDeliveryInterval")
        self.lineDeliveryInterval.setMaximumSize(QSize(160, 16777215))

        self.horizontalLayout_3.addWidget(self.lineDeliveryInterval)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_5 = QLabel(DialogNewContract)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_4.addWidget(self.label_5)

        self.lineExpirationTime = QLineEdit(DialogNewContract)
        self.lineExpirationTime.setObjectName(u"lineExpirationTime")
        self.lineExpirationTime.setMaximumSize(QSize(160, 16777215))

        self.horizontalLayout_4.addWidget(self.lineExpirationTime)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.buttonBox = QDialogButtonBox(DialogNewContract)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogNewContract)
        self.buttonBox.accepted.connect(DialogNewContract.accept)
        self.buttonBox.rejected.connect(DialogNewContract.reject)

        QMetaObject.connectSlotsByName(DialogNewContract)

    # setupUi

    def retranslateUi(self, DialogNewContract):
        DialogNewContract.setWindowTitle(
            QCoreApplication.translate("DialogNewContract", u"Dialog", None)
        )
        self.labelDescr.setText(
            QCoreApplication.translate(
                "DialogNewContract",
                u'<html><head/><body><p>Details of the <span style=" font-weight:600;">new contract</span> between agent #XXX and agent #YYY:</p></body></html>',
                None,
            )
        )
        self.label.setText(
            QCoreApplication.translate("DialogNewContract", u"Product:", None)
        )
        self.label_3.setText(
            QCoreApplication.translate(
                "DialogNewContract", u"First delivery time:", None
            )
        )
        self.label_4.setText(
            QCoreApplication.translate(
                "DialogNewContract", u"Delivery interval in steps:", None
            )
        )
        self.label_5.setText(
            QCoreApplication.translate("DialogNewContract", u"Expiration time:", None)
        )

    # retranslateUi
