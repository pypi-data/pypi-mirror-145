import typing
import logging

import fameio.source.scenario as fameio


class Agent(fameio.Agent):
    """Extends fameio.Agent with the features required for the GUI"""

    def __init__(self, agent_id: int, type_name: str):
        super().__init__(agent_id, type_name)
        self._inputs = []
        self._outputs = []
        self._display_xy = None

    @property
    def inputs(self) -> typing.List[int]:
        return self._inputs

    def add_input(self, agent_id: int) -> None:
        self._inputs.append(agent_id)

    @property
    def outputs(self) -> typing.List[int]:
        return self._outputs

    def add_output(self, agent_id: int) -> None:
        self._outputs.append(agent_id)

    @property
    def display_xy(self) -> typing.Optional[typing.List[float]]:
        return self._display_xy

    def set_display_xy(self, x: int, y: int) -> None:
        self._display_xy = [x, y]

    @classmethod
    def from_dict(cls, definitions: dict) -> "Agent":
        result = super().from_dict(definitions)
        if (
            definitions.get("ext", None) is not None
            and definitions["ext"].get("DisplayXY", None) is not None
        ):
            xy = definitions["ext"].get("DisplayXY")
            if type(xy) is list and len(xy) == 2:
                result._display_xy = [float(xy[0]), float(xy[1])]
            else:
                logging.warning(
                    "invalid 'DisplayXY' values for agent {}: {}".format(
                        result.display_id, xy
                    )
                )
        return result

    def to_dict(self) -> dict:
        result = super().to_dict()
        if self.display_xy is not None:
            result["ext"] = {"DisplayXY": self.display_xy}
        return result
