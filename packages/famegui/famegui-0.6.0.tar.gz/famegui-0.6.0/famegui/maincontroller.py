import logging
import typing
from PySide2 import QtCore

from famegui import models
from famegui.agent_controller import AgentController
from famegui.appworkingdir import AppWorkingDir
import fameio.source.validator as fameio


class ProjectProperties(QtCore.QObject):
    """Class used to attach extra properties to a scenario model and signal when they change"""

    changed = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self, file_path=""):
        self._has_unsaved_changes = False
        self._file_path = file_path
        self._validation_errors = []
        self.changed.emit()

    @property
    def has_unsaved_changes(self) -> bool:
        return self._has_unsaved_changes

    def set_unsaved_changes(self, has_changes: bool = True):
        if self._has_unsaved_changes != has_changes:
            self._has_unsaved_changes = has_changes
            self.changed.emit()

    @property
    def file_path(self) -> str:
        return self._file_path

    def set_file_path(self, file_path: str) -> None:
        if self._file_path != file_path:
            self._file_path = file_path
            self.changed.emit()

    @property
    def is_validation_successful(self) -> bool:
        return len(self._validation_errors) == 0

    @property
    def validation_errors(self) -> typing.List[str]:
        return self._validation_errors

    def clear_validation_errors(self) -> None:
        was_invalid = not self.is_validation_successful
        self._validation_errors = []
        if was_invalid:
            logging.info("schema validation status changed to valid")
            self.changed.emit()

    def set_validation_error(self, msg: str) -> None:
        assert msg != ""
        was_valid = self.is_validation_successful
        self._validation_errors = [msg]
        if was_valid:
            logging.info("schema validation status changed to invalid")
            self.changed.emit()


class MainController(QtCore.QObject):
    # agent selection update
    selected_agent_changed = QtCore.Signal(AgentController)
    # new agent added
    agent_added = QtCore.Signal(AgentController)
    # new contract added
    contract_added = QtCore.Signal(
        AgentController, AgentController, models.Contract
    )  # sender, receiver, contract

    def __init__(self, working_dir: AppWorkingDir):
        super().__init__()
        logging.debug("initializing main controller")
        self._working_dir = working_dir
        self._scenario_model = None
        self._agents = {}
        self._contracts = {}
        self._project_properties = ProjectProperties()

    def reset(self, scenario: models.Scenario = None) -> None:
        self._agents = {}
        self._contracts = {}
        self._scenario_model = scenario
        self._project_properties.reset()

    @property
    def is_open(self) -> bool:
        return self._scenario_model is not None

    @property
    def has_unsaved_changes(self) -> bool:
        return self.project_properties.has_unsaved_changes

    @property
    def project_properties(self) -> ProjectProperties:
        return self._project_properties

    @property
    def schema(self) -> models.Schema:
        return self.scenario.schema

    @property
    def scenario(self) -> models.Scenario:
        return self._scenario_model

    def update_scenario_properties(self, props: models.GeneralProperties):
        has_changed = self._scenario_model.update_properties(props)
        if has_changed:
            self._project_properties.set_unsaved_changes(True)

    @property
    def can_export_protobuf(self) -> bool:
        return (
            self.is_open
            and self.project_properties.is_validation_successful
            and not self.has_unsaved_changes
        )

    @property
    def agent_count(self) -> int:
        return len(self._agents)

    @property
    def agent_list(self) -> typing.List[AgentController]:
        return self._agents.values()

    def agent_from_id(self, id: int) -> AgentController:
        assert id in self._agents
        return self._agents[id]

    @property
    def contract_count(self) -> int:
        return len(self._contracts)

    def compute_scene_rect(self) -> QtCore.QRectF:
        rect = QtCore.QRectF(0, 0, 1000, 1000)
        for a in self.agent_list:
            margin = 20
            item_size = a.scene_item.boundingRect().width()
            left = a.scene_item.x() - margin
            right = a.scene_item.x() + item_size + margin
            top = a.scene_item.y() + -margin
            bottom = a.scene_item.y() + item_size + margin
            if left < rect.left():
                rect.setLeft(left)
            if right > rect.right():
                rect.setRight(right)
            if top < rect.top():
                rect.setTop(top)
            if bottom > rect.bottom():
                rect.setBottom(bottom)

        return rect

    def generate_new_agent_id(self):
        new_id = len(self._agents) + 1
        # note: we don't control how ids have been generated for agents created from an external source
        # so we check for possible conflict and solve it
        if new_id in self._agents:
            for i in range(1, len(self._agents) + 2):
                if i not in self._agents:
                    new_id = i
                    break
        logging.debug("generated new agent id {}".format(new_id))
        return new_id

    # the given agent id can be 0 to clear the current selection
    def set_selected_agent_id(self, agent_id: int):
        assert self.is_open
        if agent_id not in self._agents:
            assert agent_id == 0 or agent_id is None
            self.selected_agent_changed.emit(None)
        else:
            self.selected_agent_changed.emit(self._agents[agent_id])

    def add_new_agent(self, agent_model: models.Agent, x: int, y: int):
        assert self.is_open
        agent_model.set_display_xy(x, y)
        self._create_agent_controller(agent_model)
        self._scenario_model.add_agent(agent_model)
        self._project_properties.set_unsaved_changes(True)
        self.revalidate_scenario()
        logging.info(
            "created new agent {} of type '{}'".format(
                agent_model.display_id, agent_model.type_name
            )
        )

    def _create_agent_controller(self, agent_model: models.Agent):
        assert self.is_open

        # accept to add the agent even if invalid
        agent_ctrl = AgentController(agent_model)
        self._agents[agent_ctrl.id] = agent_ctrl
        agent_ctrl.model_was_modified.connect(
            self._project_properties.set_unsaved_changes
        )

        logging.info("new agent {} added".format(agent_ctrl.display_id))
        self.agent_added.emit(agent_ctrl)

    def add_new_contract(self, contract_model: models.Contract):
        self._scenario_model.add_contract(contract_model)
        self._create_contract_model(contract_model)
        self._project_properties.set_unsaved_changes(True)
        self.revalidate_scenario()
        logging.info(
            "created new contract '{}' between {} and {}".format(
                contract_model.product_name,
                contract_model.display_sender_id,
                contract_model.display_receiver_id,
            )
        )

    def _create_contract_model(self, contract: models.Contract):
        assert self.is_open

        # validate sender / receiver are known
        if contract.sender_id not in self._agents:
            raise ValueError(
                "can't add contract '{}' because sender agent id '{}' is unknown".format(
                    contract.product_name, contract.sender_id
                )
            )

        if contract.receiver_id not in self._agents:
            raise ValueError(
                "can't add contract '{}' because receiver agent id '{}' is unknown".format(
                    contract.product_name, contract.receiver_id
                )
            )

        sender_ctrl = self._agents[contract.sender_id]
        receiver_ctrl = self._agents[contract.receiver_id]

        # connect agents
        sender_ctrl.model.add_output(contract.receiver_id)
        receiver_ctrl.model.add_input(contract.sender_id)

        self.contract_added.emit(sender_ctrl, receiver_ctrl, contract)

    def revalidate_scenario(self):
        assert self._scenario_model is not None
        try:
            fameio.SchemaValidator.ensure_is_valid_scenario(self._scenario_model)
            self._project_properties.clear_validation_errors()
        except fameio.ValidationException as e:
            err_msg = str(e)
            logging.warning("failed to validate the scenario: {}".format(err_msg))
            self._project_properties.set_validation_error(err_msg)

    def init_scenario_model(self, scenario: models.Scenario, file_path: str):
        logging.debug("opening new scenario")
        self.reset()

        try:
            self._scenario_model = scenario
            self._project_properties.reset(file_path)
            self._project_properties.set_unsaved_changes(True)

            # process and validate the scenario
            for a in self._scenario_model.agents:
                self._create_agent_controller(a)
            for c in self._scenario_model.contracts:
                self._create_contract_model(c)

            self.revalidate_scenario()
        except Exception as e:
            logging.error("failed to init the given scenario: {}".format(e))
            self.reset()
            raise

        # refresh the UI
        self._project_properties.changed.emit()

    def save_to_file(self, file_path):
        assert self.is_open
        models.ScenarioLoader.save_to_yaml_file(self._scenario_model, file_path)
        # update status
        self._project_properties.set_unsaved_changes(False)
        self._project_properties.set_file_path(file_path)
        self.revalidate_scenario()
