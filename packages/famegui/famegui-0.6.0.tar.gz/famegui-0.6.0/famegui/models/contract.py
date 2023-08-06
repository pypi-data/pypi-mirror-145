import fameio.source.scenario as fameio


class Contract(fameio.Contract):
    """Extends fameio.Contract with the features required for the GUI"""

    @classmethod
    def from_dict(cls, definitions: dict) -> "Contract":
        return super().from_dict(definitions)
