import logging
import typing

import fameio.source.scenario as fameio
import fameio.source.schema as fameio_schema
import famegui.models as models


class Scenario(fameio.Scenario):
    def __init__(self, schema: fameio_schema.Schema, props: fameio.GeneralProperties):
        super().__init__(schema, props)

    def set_agent_display_xy(self, agent_id: int, x: int, y: int) -> None:
        for a in self.agents:
            if a.id == agent_id:
                a.set_display_xy(x, y)
                return
        raise RuntimeError("unknown agent '#{}'".format(agent_id))

    def update_properties(self, props: models.GeneralProperties) -> bool:
        """Sync the scenario properties with the given ones, returns True if some changes"""
        if props.to_dict() != self.general_properties.to_dict():
            logging.info("updating scenario general properties")
            self._general_props = props
            return True
        return False

    def add_contract(self, contract: models.Contract) -> None:
        # TODO: move here the logic located in MainController._create_contract_model
        super().add_contract(contract)

    @property
    def agents(self) -> typing.List[models.Agent]:
        return super().agents
