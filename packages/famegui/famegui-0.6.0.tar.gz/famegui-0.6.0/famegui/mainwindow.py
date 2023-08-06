# This Python file uses the following encoding: utf-8
import os
import logging
import getpass

from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtCore, QtGui, QtWidgets

from famegui import models
import famegui.generated.qt_resources_rc
from famegui.generated.ui_mainwindow import Ui_MainWindow
from famegui.dialog_scenario_properties import DialogScenarioProperties
from famegui.dialog_newagent import DialogNewAgent
from famegui.dialog_newcontract import DialogNewContract
from famegui.scenario_graph_view import ScenarioGraphView
from famegui.agent_controller import AgentController
from famegui.maincontroller import MainController
from famegui.appworkingdir import AppWorkingDir
from famegui.path_resolver import FameGuiPathResolver
import fameio.source.scenario.attribute as fameio


class PropertyTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(
        self,
        parent: QtWidgets.QTreeWidget,
        attr_name: str,
        attr_value: fameio.Attribute,
    ):
        super().__init__(parent, [attr_name, str(attr_value.value)])
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)

    def setData(self, column, role, value):
        """Override QTreeWidgetItem.setData()"""
        if role == QtCore.Qt.EditRole:
            # review: Can we remove this code? It seems to be unused at the moment and not necessary.
            # logging.info("new value: {}".format(value))
            pass

        QtWidgets.QTreeWidgetItem.setData(self, column, role, value)


class MainWindow(QMainWindow):
    def __init__(self, working_dir: AppWorkingDir):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._working_dir = working_dir
        self._path_resolver = FameGuiPathResolver(self._working_dir)
        self._tree_items_for_agent_types = {}
        self._controller = MainController(self._working_dir)
        # init
        self._init_ui()
        self._connect_actions()
        self._connect_slots()
        self._on_project_closed()

    def _init_ui(self):
        logging.debug("initializing main window UI")
        self.setWindowIcon(QtGui.QIcon(":/icons/nodes-128px.png"))
        # create and attach the scene
        self._graph_view = ScenarioGraphView(self)
        self._graph_view.setSceneRect(self._controller.compute_scene_rect())
        self.ui.graphicsView.setScene(self._graph_view)
        # customize main window
        self.ui.labelUserName.setText(getpass.getuser())
        self.ui.graphicsView.setBackgroundBrush(QtGui.QColor(230, 230, 230))
        self.setWindowTitle(QtWidgets.QApplication.instance().applicationDisplayName())
        # allowed zoom range
        self.ui.sliderZoomFactor.setRange(10, 100)
        # status bar
        self._status_label_icon = QtWidgets.QLabel()
        self.statusBar().addWidget(self._status_label_icon)
        # project structure tree view
        self.ui.treeProjectStructure.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self.ui.treeProjectStructure.setColumnCount(1)
        self.ui.treeProjectStructure.setHeaderLabels(["Agents"])
        # attributes tree view
        self.ui.treeAttributes.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self.ui.treeAttributes.setRootIsDecorated(False)
        self.ui.treeAttributes.setColumnCount(2)
        self.ui.treeAttributes.setHeaderLabels(["Attribute", "Value"])
        self.ui.treeAttributes.setColumnWidth(0, 140)
        self.ui.treeAttributes.setAlternatingRowColors(True)
        self.ui.treeAttributes.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )

    def _connect_actions(self):
        logging.debug("connecting main window actions")
        # new
        self.ui.actionNewProject.triggered.connect(self.new_project)
        # open
        self.ui.actionOpenProject.triggered.connect(self.show_open_scenario_file_dlg)
        # save (enabled only when a change has been done)
        self.ui.actionSaveProject.triggered.connect(self.save_project)
        # save as
        self.ui.actionSaveProjectAs.triggered.connect(self.save_project_as)
        # close
        self.ui.actionCloseProject.triggered.connect(self.close_project)
        # generate protobuf
        self.ui.actionMakeRunConfig.triggered.connect(self.make_run_config)
        # exit
        self.ui.actionExit.triggered.connect(self.close)
        # edit
        self.ui.actionGeneralProperties.triggered.connect(
            self._on_edit_scenario_properties
        )

    def _connect_slots(self):
        logging.debug("initializing main window slots")
        # ui
        self.ui.sliderZoomFactor.valueChanged.connect(self._on_zoom_value_changed)
        self._graph_view.selected_agent_changed.connect(
            self._controller.set_selected_agent_id
        )
        self._graph_view.contract_creation_requested.connect(
            self._on_contract_creation_requested
        )
        self._graph_view.agent_creation_requested.connect(
            self._on_agent_creation_requested
        )
        self.ui.treeProjectStructure.currentItemChanged.connect(
            self._on_tree_view_current_item_changed
        )
        self.ui.lineFilterPattern.textChanged.connect(self._filter_pattern_changed)
        self._graph_view.zoom_in_requested.connect(
            lambda: self.ui.sliderZoomFactor.setValue(
                self.ui.sliderZoomFactor.value() + 10
            )
        )
        self._graph_view.zoom_out_requested.connect(
            lambda: self.ui.sliderZoomFactor.setValue(
                self.ui.sliderZoomFactor.value() - 10
            )
        )
        # controller
        self._controller.project_properties.changed.connect(
            self._on_scenario_status_changed
        )
        self._controller.agent_added.connect(self._on_agent_added)
        self._controller.contract_added.connect(self._on_contract_added)
        self._controller.selected_agent_changed.connect(self._on_selected_agent_changed)

    def _on_zoom_value_changed(self):
        zoom_factor = self.ui.sliderZoomFactor.value()
        assert zoom_factor > 0
        scale_factor = zoom_factor * 0.01
        self.ui.graphicsView.setTransform(
            QtGui.QTransform.fromScale(scale_factor, scale_factor)
        )
        self.ui.labelZoomFactor.setText("{} %".format(zoom_factor))

    def _on_tree_view_current_item_changed(self):
        assert self._controller.is_open

        selected_agent_id = None

        tree_item = self.ui.treeProjectStructure.currentItem()
        if tree_item is not None:
            # note: the given id value can be None
            selected_agent_id = tree_item.data(0, QtCore.Qt.UserRole)

        self._controller.set_selected_agent_id(selected_agent_id)

    def _on_agent_creation_requested(self, x: int, y: int):
        assert self._controller.is_open

        dlg = DialogNewAgent(self._controller.schema, self._working_dir, self)
        if dlg.exec_() != 0:
            new_agent = dlg.make_new_agent(self._controller.generate_new_agent_id())
            self._controller.add_new_agent(new_agent, x, y)
            self._graph_view.setSceneRect(self._controller.compute_scene_rect())

    def _on_contract_creation_requested(self, sender_id: int, receiver_id: int):
        sender = self._controller.agent_from_id(sender_id)
        receiver = self._controller.agent_from_id(receiver_id)
        dlg = DialogNewContract(
            sender, receiver, self._controller.scenario.schema, self
        )
        if dlg.exec_() != 0:
            self._controller.add_new_contract(dlg.make_new_contract())

    def _on_selected_agent_changed(self, agent_ctrl: AgentController):
        if agent_ctrl is None:
            # clear selection
            self.ui.treeProjectStructure.clearSelection()
            self._graph_view.clearSelection()
            self.ui.treeAttributes.clear()
            return

        # block signals
        self.ui.treeProjectStructure.blockSignals(True)
        self._graph_view.blockSignals(True)

        # update graph view
        self._graph_view.clearSelection()
        agent_ctrl.scene_item.setSelected(True)
        # update tree view
        self.ui.treeProjectStructure.setCurrentItem(agent_ctrl.tree_item)
        # update agent view
        self.ui.treeAttributes.clear()
        item_type = QtWidgets.QTreeWidgetItem(
            self.ui.treeAttributes, ["Type", agent_ctrl.type_name]
        )
        item_type.setBackgroundColor(1, agent_ctrl.svg_color)
        QtWidgets.QTreeWidgetItem(self.ui.treeAttributes, ["ID", agent_ctrl.display_id])
        for attr_name, attr_value in agent_ctrl.attributes.items():
            PropertyTreeItem(self.ui.treeAttributes, attr_name, attr_value)

        # unblock signals
        self.ui.treeProjectStructure.blockSignals(False)
        self._graph_view.blockSignals(False)

    def _filter_pattern_changed(self):
        pattern = self.ui.lineFilterPattern.text().lower()
        for a in self._controller.agent_list:
            hide = a.type_name.lower().find(pattern) == -1
            a.tree_item.setHidden(hide)

    def _tree_item_parent_for_agent(self, agent_ctrl) -> QtWidgets.QTreeWidgetItem:
        # return existing if it already exists
        if agent_ctrl.type_name in self._tree_items_for_agent_types:
            return self._tree_items_for_agent_types[agent_ctrl.type_name]
        item = QtWidgets.QTreeWidgetItem(
            self.ui.treeProjectStructure, [agent_ctrl.type_name]
        )
        item.setExpanded(True)
        item.setBackgroundColor(0, agent_ctrl.svg_color)
        self._tree_items_for_agent_types[agent_ctrl.type_name] = item
        return item

    def _create_agent_tree_item(self, agent_ctrl: AgentController):
        parent_item = self._tree_item_parent_for_agent(agent_ctrl)
        # create tree item
        item = QtWidgets.QTreeWidgetItem(parent_item, [agent_ctrl.display_id])
        item.setBackgroundColor(0, QtGui.QColor(agent_ctrl.svg_color))
        item.setData(0, QtCore.Qt.UserRole, agent_ctrl.id)
        item.setToolTip(0, agent_ctrl.tooltip_text)
        # add item
        agent_ctrl.tree_item = item
        self.ui.treeProjectStructure.addTopLevelItem(item)

    def _on_agent_added(self, agent_ctrl: AgentController):
        logging.debug("agent_added: {}".format(agent_ctrl.display_id))
        self._graph_view.add_agent(agent_ctrl)
        self._create_agent_tree_item(agent_ctrl)

    def _on_contract_added(
        self,
        sender: AgentController,
        receiver: AgentController,
        contract: models.Contract,
    ):
        # update scene graph
        self._graph_view.add_contract(sender, receiver)
        # update tree view
        sender_tree_item = QtWidgets.QTreeWidgetItem(
            sender.tree_item,
            ["{} ({})".format(receiver.display_id, contract.product_name)],
        )
        sender_tree_item.setIcon(0, QtGui.QIcon(u":/icons/16px-login.png"))
        receiver_tree_item = QtWidgets.QTreeWidgetItem(
            receiver.tree_item,
            ["{} ({})".format(sender.display_id, contract.product_name)],
        )
        receiver_tree_item.setIcon(0, QtGui.QIcon(u":/icons/16px-logout.png"))

    def _confirm_current_project_can_be_closed(self) -> bool:
        if self._controller.has_unsaved_changes:
            choice = QtWidgets.QMessageBox.warning(
                self,
                self.tr("Modifications will be lost"),
                self.tr(
                    "Modifications done to the current scenario have not been saved!\n\nWhat do you want to do?"
                ),
                QtWidgets.QMessageBox.StandardButtons(
                    QtWidgets.QMessageBox.Save
                    | QtWidgets.QMessageBox.Discard
                    | QtWidgets.QMessageBox.Cancel
                ),
                QtWidgets.QMessageBox.Cancel,
            )
            if choice == QtWidgets.QMessageBox.Save:
                return self.save_project()
            elif choice == QtWidgets.QMessageBox.Discard:
                return True
            else:
                return False
        return True

    def _on_project_closed(self):
        self._graph_view.clear()
        # reset zoom
        self.ui.sliderZoomFactor.setValue(50)
        # reset attributes
        self._tree_items_for_agent_types = {}
        # reset scenario
        self._controller.reset()
        # reset ui
        self.ui.treeProjectStructure.clear()
        self.ui.treeAttributes.clear()
        self.ui.lineFilterPattern.clear()
        self.ui.labelProjectName.clear()

    def display_error_msg(self, msg: str) -> None:
        logging.error(msg)
        if not msg.endswith("."):
            msg += "."
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), msg)

    def new_project(self):
        if not self._confirm_current_project_can_be_closed():
            return
        self._on_project_closed()

        dlg = DialogScenarioProperties(
            models.GeneralProperties.make_default(), self._working_dir, self
        )
        dlg.setWindowTitle(self.tr("New scenario"))
        # ask user to choose which schema to use for that new scenario
        dlg.enable_schema_selection()

        if dlg.exec_() != 0:
            schema_path = dlg.get_selected_schema_full_path()
            schema = models.Schema.load_yaml_file(schema_path)
            scenario = models.Scenario(schema, dlg.make_properties())
            self._controller.reset(scenario)

    def save_project(self) -> bool:
        if not self._controller.is_open:
            return False
        return self._do_save_project_as(self._controller.project_properties.file_path)

    def save_project_as(self) -> bool:
        if not self._controller.is_open:
            return False
        return self._do_save_project_as("")

    def _do_save_project_as(self, file_path: str) -> bool:
        assert self._controller.is_open

        if file_path == "":
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self,
                self.tr("Save scenario file"),
                self._working_dir.scenarios_dir,
                "Scenario file (*.yaml *.yml)",
            )
            if file_path == "":
                return False

        self._controller.save_to_file(file_path)
        self._graph_view.setSceneRect(self._controller.compute_scene_rect())
        return True

    def close_project(self) -> None:
        if self._confirm_current_project_can_be_closed():
            self._on_project_closed()

    def show_open_scenario_file_dlg(self):
        if not self._confirm_current_project_can_be_closed():
            return

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Open scenario file"),
            self._working_dir.scenarios_dir,
            self.tr("Scenario (*.yaml *.yml)"),
        )
        if file_path != "":
            self.load_scenario_file(file_path)

    def _on_scenario_status_changed(self):
        logging.debug(
            "scenario status changed: agents={}, contracts={}".format(
                self._controller.agent_count, self._controller.contract_count
            )
        )

        is_open = self._controller.is_open
        self.ui.treeProjectStructure.setEnabled(is_open)
        self.ui.treeAttributes.setEnabled(is_open)
        self.ui.lineFilterPattern.setEnabled(is_open)
        self.ui.graphicsView.setEnabled(is_open)
        self.ui.sliderZoomFactor.setEnabled(is_open)

        props = self._controller.project_properties
        if is_open:
            if props.file_path != "":
                self.ui.labelProjectName.setText(props.file_path)
            else:
                self.ui.labelProjectName.setText(self.tr("Unsaved scenario"))
        else:
            self.ui.labelProjectName.setText("")

        self.ui.actionSaveProject.setEnabled(props.has_unsaved_changes)
        self.ui.actionGeneralProperties.setEnabled(is_open)
        self.ui.actionMakeRunConfig.setEnabled(self._controller.can_export_protobuf)

        # update status bar
        if self._controller.agent_count > 0:
            if props.is_validation_successful:
                self._status_label_icon.setPixmap(":/icons/success-16px.png")
                self._status_label_icon.setToolTip(
                    self.tr("Schema validation succeeded")
                )
            else:
                self._status_label_icon.setPixmap(":/icons/warning-16px.png")
                all_errors = "\n".join(props.validation_errors)
                self._status_label_icon.setToolTip(
                    self.tr("Schema validation failed:\n{}".format(all_errors))
                )
        else:
            self._status_label_icon.clear()

    def load_scenario_file(self, file_path):
        self._on_project_closed()
        file_path = os.path.abspath(file_path)
        try:
            logging.info("opening scenario file {}".format(file_path))
            scenario_model = models.ScenarioLoader.load_yaml_file(
                file_path, self._path_resolver
            )
            self._controller.init_scenario_model(scenario_model, file_path)
        except Exception as e:
            self._on_project_closed()
            self.display_error_msg("Failed to open scenario file: {}".format(e))
            return

        props = self._controller.project_properties
        if not props.is_validation_successful:
            QtWidgets.QMessageBox.warning(
                self,
                self.tr("Validation failure"),
                self.tr("The loaded scenario does not fulfill the schema:\n\n")
                + "\n".join(props.validation_errors),
            )

    def _on_edit_scenario_properties(self):
        dlg = DialogScenarioProperties(
            self._controller.scenario.general_properties, self._working_dir, self
        )
        dlg.setWindowTitle(self.tr("Scenario properties"))
        if dlg.exec_() != 0:
            self._controller.update_scenario_properties(dlg.make_properties())

    def make_run_config(self):
        assert self._controller.can_export_protobuf
        scenario_name = os.path.basename(
            self._controller.project_properties.file_path
        ).replace(".yaml", "")
        output_path = "{}/{}.pb".format(self._working_dir.protobuf_dir, scenario_name)
        output_path = self._working_dir.make_relative_path(output_path)

        dlg = DialogScenarioProperties(
            self._controller.scenario.general_properties, self._working_dir, self
        )
        dlg.setWindowTitle(self.tr("Make run config"))
        dlg.enable_outputfile_selection(output_path)
        if dlg.exec_() != 0:
            self._controller.update_scenario_properties(dlg.make_properties())
            self.save_project()
            output_path = self._working_dir.make_full_path(dlg.get_output_file_path())

            # display progress dialog
            progress_dlg = QtWidgets.QProgressDialog(self)
            progress_dlg.setLabelText(self.tr("Generating protobuf file..."))
            progress_dlg.setRange(0, 0)
            progress_dlg.setCancelButton(None)
            progress_dlg.show()
            QApplication.processEvents()

            try:
                models.write_protobuf_output(
                    self._controller.scenario, output_path, self._path_resolver
                )
                progress_dlg.close()
                QtWidgets.QMessageBox.information(
                    self,
                    self.tr("Success"),
                    self.tr(
                        "The following file was successfully generated:\n\n{}"
                    ).format(output_path),
                )
            except Exception as e:
                progress_dlg.close()
                logging.error("failed to generate protobuf output: {}".format(e))
                QtWidgets.QMessageBox.critical(
                    self,
                    self.tr("Error"),
                    self.tr("Failed to generate the protobuf output.\n\n{}").format(e),
                )
            finally:
                progress_dlg.close()

    # prevent data loss when closing the main window
    def closeEvent(self, event):
        if not self._confirm_current_project_can_be_closed():
            event.ignore()
        else:
            event.accept()
