from PySide2.QtWidgets import QDialog, QDialogButtonBox, QLineEdit
from PySide2 import QtCore, QtGui

from .generated.ui_dialog_newcontract import Ui_DialogNewContract

from famegui import models
from famegui.agent_controller import AgentController


class DialogNewContract(QDialog):
    def _configure_line_edit_for_unsigned_int(self, line_edit: QLineEdit):
        line_edit.setText("0")
        regex_uint64 = QtCore.QRegExp("\\d{1,20}")
        line_edit.setValidator(QtGui.QRegExpValidator(regex_uint64))
        line_edit.textChanged.connect(self._update_ok_button_status)

    def _configure_line_edit_for_signed_int(self, line_edit: QLineEdit):
        line_edit.setText("0")
        regex_uint64 = QtCore.QRegExp("-?\\d{1,20}")
        line_edit.setValidator(QtGui.QRegExpValidator(regex_uint64))
        line_edit.textChanged.connect(self._update_ok_button_status)

    def _configure_line_edit_for_optional_signed_int(self, line_edit: QLineEdit):
        line_edit.setText("")
        line_edit.setPlaceholderText(self.tr("optional"))
        regex_uint64 = QtCore.QRegExp("-?\\d{0,20}")
        line_edit.setValidator(QtGui.QRegExpValidator(regex_uint64))

    def __init__(
        self,
        sender: AgentController,
        receiver: AgentController,
        schema: models.Schema,
        parent=None,
    ):
        QDialog.__init__(self, parent)
        self._ui = Ui_DialogNewContract()
        self._ui.setupUi(self)
        self._sender = sender
        self._receiver = receiver

        self.setWindowTitle(self.tr("New contract"))
        self._ui.labelDescr.setText(
            self.tr(
                "<html><head/><body>"
                "<p>Create new contract between:</p>"
                "<ul>"
                "<li>Sender: agent <b>{}</b> of type <b>{}</b></li>"
                "<li>Receiver: agent <b>{}</b> of type <b>{}</b></li>"
                "</ul>"
                "</body></html>"
            ).format(
                sender.display_id,
                sender.type_name,
                receiver.display_id,
                receiver.type_name,
            )
        )

        # accept uint64 numbers as specified in protobuf schema
        self._configure_line_edit_for_unsigned_int(self._ui.lineDeliveryInterval)
        self._configure_line_edit_for_signed_int(self._ui.lineFirstDeliveryTime)
        self._configure_line_edit_for_optional_signed_int(self._ui.lineExpirationTime)

        # fill possible products to select based on the sender schema agent type
        sender_type = schema.agent_type_from_name(sender.type_name)
        assert sender_type is not None
        self._ui.comboBoxProduct.addItems(sender_type.products)

        # force the user to select a product except if only one is available
        if self._ui.comboBoxProduct.count() != 1:
            self._ui.comboBoxProduct.setCurrentIndex(-1)

        self._ui.comboBoxProduct.currentIndexChanged.connect(
            self._update_ok_button_status
        )
        self._update_ok_button_status()

    def make_new_contract(self) -> models.Contract:
        expiration_time_str = self._ui.lineExpirationTime.text()
        expiration_time = int(expiration_time_str) if expiration_time_str else None

        return models.Contract(
            self._sender.id,
            self._receiver.id,
            self._ui.comboBoxProduct.currentText(),
            int(self._ui.lineDeliveryInterval.text()),
            int(self._ui.lineFirstDeliveryTime.text()),
            expiration_time,
        )

    def _update_ok_button_status(self):
        all_fields_ok = (
            self._ui.comboBoxProduct.currentText() != ""
            and self._ui.lineDeliveryInterval.text() != ""
            and self._ui.lineFirstDeliveryTime.text() != ""
        )
        self._ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(all_fields_ok)
