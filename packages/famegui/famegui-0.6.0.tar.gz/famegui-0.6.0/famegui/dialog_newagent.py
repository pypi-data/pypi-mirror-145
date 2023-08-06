import logging
import os
import typing
from PySide2 import QtCore, QtGui, QtWidgets

from .generated.ui_dialog_newagent import Ui_DialogNewAgent
from famegui import models
from famegui.appworkingdir import AppWorkingDir
import fameio.source.schema as schema
import fameio.source.scenario as fameio


class FileChooserWidget(QtWidgets.QWidget):
    current_value_changed = QtCore.Signal(str)

    def __init__(
        self, working_dir: AppWorkingDir, parent: QtWidgets.QWidget = None
    ) -> None:
        QtWidgets.QWidget.__init__(self, parent)
        self._working_dir = working_dir
        # layout
        layout = QtWidgets.QHBoxLayout(self)
        layout.setMargin(0)
        layout.setSpacing(0)
        # line edit (file path)
        self._line_edit = QtWidgets.QLineEdit(self)
        self._line_edit.setPlaceholderText(
            self.tr("Please enter file path or single float value")
        )
        self._line_edit.textChanged.connect(self._on_text_edit_changed)
        layout.addWidget(self._line_edit)
        # button (to open dialog box)
        button = QtWidgets.QPushButton("...", self)
        button.setToolTip(self.tr("Select file..."))
        button.setFixedWidth(button.fontMetrics().width(button.text()) + 10)
        layout.addWidget(button)
        # connect
        button.clicked.connect(self._on_button_clicked)

    def _on_button_clicked(self) -> None:
        open_location = self._working_dir.timeseries_dir
        if self._line_edit.text() != "":
            full_edit_path = self._working_dir.make_full_path(self._line_edit.text())
            if os.path.isfile(full_edit_path):
                open_location = full_edit_path

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Open time series file"),
            open_location,
            self.tr("Time series (*.csv);;All files (*.*)"),
        )
        if file_path != "":
            file_path = self._working_dir.make_relative_path(file_path)
            self._line_edit.setText(file_path)

    def _on_text_edit_changed(self, value: str) -> None:
        self.current_value_changed.emit(value)

    def display_error(self, has_error: bool) -> None:
        style_sheet = "QLineEdit { background: '#F66257'; }" if has_error else ""
        self._line_edit.setStyleSheet(style_sheet)


class AttributeTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(
        self,
        parent: QtWidgets.QTreeWidget,
        attr_name: str,
        attr_spec: schema.AttributeSpecs,
        working_dir: AppWorkingDir,
    ):
        self._attr_name = attr_name
        self._attr_spec = attr_spec
        self._working_dir = working_dir
        self._attr_value = None
        self._display_error = lambda has_error: None

        QtWidgets.QTreeWidgetItem.__init__(self, parent, [attr_name])

        font = self.font(0)
        if self._attr_spec.is_mandatory:
            font.setBold(True)
            tooltip = self.tr("{} (mandatory)").format(self._attr_name)
        else:
            font.setItalic(True)
            tooltip = self.tr("{} (optional)").format(self._attr_name)
        self.setFont(0, font)
        self.setToolTip(0, tooltip)

        parent.setItemWidget(self, 1, self._create_edit_widget())

    @property
    def attr_name(self) -> str:
        return self._attr_name

    @property
    def attr_value(self) -> typing.Any:
        return self._attr_value

    @property
    def validation_error(self) -> typing.Optional[str]:
        if self._attr_spec.is_mandatory and self._attr_value is None:
            return "mandatory attribute '{}' is missing".format(self.attr_name)
        return None

    _supported_list_types = [
        schema.AttributeType.INTEGER,
        schema.AttributeType.LONG,
        schema.AttributeType.DOUBLE,
    ]

    @property
    def _attr_enum_values(self) -> typing.List[str]:
        """Returns the enum values of the attached AttributeSpecs"""
        assert self._attr_spec.attr_type == schema.AttributeType.ENUM
        assert not self._attr_spec.is_list
        assert not self._attr_spec.has_nested_attributes
        return self._attr_spec.values

    def _create_edit_widget(self) -> QtWidgets.QWidget:
        spec = self._attr_spec

        # TODO: see how to handle default values
        assert not spec.has_default_value

        # TODO: handle nested and block types
        if spec.has_nested_attributes:
            return self._create_unsupported_edit_widget("Nested attributes")

        # list
        if spec.is_list:
            if spec.attr_type not in self._supported_list_types:
                return self._create_unsupported_edit_widget(
                    "List of {}".format(spec.attr_type)
                )
            return self._create_list_edit(spec.attr_type)

        if spec.attr_type == schema.AttributeType.ENUM:
            combo_box = QtWidgets.QComboBox()
            enum_values = self._attr_enum_values
            combo_box.addItems(enum_values)
            if len(enum_values) == 1:
                combo_box.setCurrentIndex(0)
                self._attr_value = enum_values[0]
            else:
                combo_box.setCurrentIndex(-1)
            combo_box.currentTextChanged.connect(self._on_enum_value_changed)
            return combo_box
        elif spec.attr_type == schema.AttributeType.TIME_SERIES:
            file_chooser = FileChooserWidget(self._working_dir)
            file_chooser.current_value_changed.connect(
                self._on_time_series_value_changed
            )
            self._display_error = file_chooser.display_error
            return file_chooser
        elif (
            spec.attr_type == schema.AttributeType.INTEGER
            or spec.attr_type == schema.AttributeType.LONG
        ):
            line_edit = self._create_line_edit("0", self._on_integer_value_changed)
            line_edit.setValidator(QtGui.QIntValidator())
            return line_edit
        elif spec.attr_type == schema.AttributeType.DOUBLE:
            line_edit = self._create_line_edit("0.0", self._on_double_value_changed)
            validator = QtGui.QDoubleValidator()
            # accept '.' as decimal separator
            validator.setLocale(QtCore.QLocale.English)
            line_edit.setValidator(validator)
            return line_edit
        else:
            # TODO: handle TIME_STAMP, STRING, BLOCK
            return self._create_unsupported_edit_widget(str(spec.attr_type))

    def _create_line_edit(self, placeholder_text: str, handler) -> QtWidgets.QLineEdit:
        line_edit = QtWidgets.QLineEdit()
        line_edit.setPlaceholderText(placeholder_text)
        line_edit.textChanged.connect(handler)
        self._display_error = (
            lambda has_error: line_edit.setStyleSheet(
                "QLineEdit { background: '#F66257'; }"
            )
            if has_error
            else line_edit.setStyleSheet("")
        )
        return line_edit

    def _create_list_edit(self, attr_type: schema.AttributeType) -> QtWidgets.QWidget:
        assert attr_type in self._supported_list_types
        placeholders = {
            schema.AttributeType.INTEGER: "1, 3, 5",
            schema.AttributeType.LONG: "1, 3, 5",
            schema.AttributeType.DOUBLE: "1.0, 2.5, 5",
        }
        assert len(placeholders) == len(self._supported_list_types)

        line_edit = QtWidgets.QLineEdit()
        line_edit.setPlaceholderText(placeholders[attr_type])
        line_edit.textChanged.connect(self._on_list_value_changed)
        self._display_error = (
            lambda has_error: line_edit.setStyleSheet(
                "QLineEdit { background: '#F66257'; }"
            )
            if has_error
            else line_edit.setStyleSheet("")
        )
        return line_edit

    def _create_unsupported_edit_widget(self, type_name: str) -> QtWidgets.QLabel:
        logging.error(
            "can't edit type {} because it is not supported by the GUI".format(
                type_name
            )
        )
        label = QtWidgets.QLabel()
        label.setText(
            self.tr("Editing values of type '{}' is not supported".format(type_name))
        )
        label.setStyleSheet("QLabel { background-color : #F66257; }")
        return label

    def _on_enum_value_changed(self, value: str):
        assert value == "" or value in self._attr_spec.values
        self._attr_value = value if value != "" else None

    @staticmethod
    def _is_float(value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _on_time_series_value_changed(self, value: str):
        self._display_error(False)
        if value == "":
            self._attr_value = None
        elif self._is_float(value):
            self._attr_value = float(value)
        else:
            self._attr_value = value
            if self._working_dir.find_existing_child_file(value) is None:
                self._display_error(True)

    def _on_integer_value_changed(self, value: str):
        try:
            self._attr_value = int(value) if value != "" else None
            self._display_error(False)
        except:
            self._display_error(True)
            logging.warning(
                "invalid integer value '{}' for attribute '{}'".format(
                    value, self._attr_name
                )
            )
            self._attr_value = None

    def _on_double_value_changed(self, value: str):
        try:
            self._attr_value = float(value) if value != "" else None
            self._display_error(False)
        except:
            self._display_error(True)
            logging.warning(
                "invalid double value '{}' for attribute '{}'".format(
                    value, self._attr_name
                )
            )
            self._attr_value = None

    def _on_list_value_changed(self, value: str):
        self._attr_value = None
        self._display_error(False)
        if value == "":
            return

        try:
            self._attr_value = []
            for item in value.split(","):
                # TODO: check / cast the type of each item in the string
                self._attr_value.append(item.strip())
        except:
            self._attr_value = None
            self._display_error(True)
            logging.warning(
                "invalid list value '{}' for attribute '{}'".format(
                    value, self._attr_name
                )
            )

    def tr(self, msg: str) -> str:
        return QtCore.QCoreApplication.translate("AttributeTreeItem", msg)


class DialogNewAgent(QtWidgets.QDialog):
    def __init__(self, schema: models.Schema, working_dir: AppWorkingDir, parent=None):
        QtWidgets.QDialog.__init__(self, parent=None)
        self._ui = Ui_DialogNewAgent()
        self._ui.setupUi(self)
        self._schema = schema
        self._working_dir = working_dir
        self._tree_items = []
        # init
        self.setWindowTitle(self.tr("New agent"))
        self._ui.comboBoxType.addItems(self._schema.agent_types.keys())

        # tree view
        self._ui.treeWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self._ui.treeWidget.setRootIsDecorated(False)
        self._ui.treeWidget.setColumnCount(2)
        self._ui.treeWidget.setHeaderLabels([self.tr("Attribute"), self.tr("Value")])
        self._ui.treeWidget.setColumnWidth(0, 200)
        self._ui.treeWidget.setAlternatingRowColors(True)
        self._reset_attributes()

        # connect slots
        self._ui.comboBoxType.currentTextChanged.connect(self._reset_attributes)

    def accept(self):
        if self._confirm_attributes_are_valid():
            super().accept()

    def _reset_attributes(self):
        self._ui.treeWidget.clear()
        self._tree_items.clear()

        current_agent_type = self._ui.comboBoxType.currentText()
        for attr_name, attr_spec in self._schema.agent_types[
            current_agent_type
        ].attributes.items():
            item = AttributeTreeItem(
                self._ui.treeWidget, attr_name, attr_spec, self._working_dir
            )
            self._tree_items.append(item)

    def _confirm_attributes_are_valid(self) -> bool:
        errors = ""
        for item in self._tree_items:
            if item.validation_error != None:
                errors += "- {}\n".format(item.validation_error)

        if errors == "":
            return True

        choice = QtWidgets.QMessageBox.warning(
            self,
            self.tr("All attributes are not valid"),
            self.tr(
                "The new agent won't be valid:\n{}\nDo you want to continue?".format(
                    errors
                )
            ),
            QtWidgets.QMessageBox.StandardButtons(
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            ),
            QtWidgets.QMessageBox.No,
        )
        return choice == QtWidgets.QMessageBox.Yes

    def make_new_agent(self, agent_id) -> models.Agent:
        agent_type = self._ui.comboBoxType.currentText()
        agent = models.Agent(agent_id, agent_type)
        for item in self._tree_items:
            if item.attr_value is not None:
                attr = fameio.Attribute(item.attr_name, item.attr_value)
                agent.add_attribute(item.attr_name, attr)
        return agent
