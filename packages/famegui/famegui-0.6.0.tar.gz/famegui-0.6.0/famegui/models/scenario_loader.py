import logging
import os
import yaml

import famegui.models as models
import fameio.source.loader as fameio


def _check_all_agents_have_display_coords(scenario: models.Scenario):
    if len(scenario.agents) == 0:
        return True
    for a in scenario.agents:
        if a.display_xy is None:
            return False
        return True


class CustomFameIOFactory:
    @staticmethod
    def new_schema_from_dict(definitions: dict) -> models.Schema:
        return models.Schema.from_dict(definitions)

    @staticmethod
    def new_general_properties_from_dict(definitions: dict) -> models.GeneralProperties:
        return models.GeneralProperties.from_dict(definitions)

    @staticmethod
    def new_agent_from_dict(definitions: dict) -> models.Agent:
        return models.Agent.from_dict(definitions)

    @staticmethod
    def new_contract_from_dict(definitions: dict) -> models.Contract:
        return models.Contract.from_dict(definitions)


class ScenarioLoader:
    @staticmethod
    def load_yaml_file(
        file_path: str, path_resolver: fameio.PathResolver
    ) -> models.Scenario:
        """Load (read and parse) a YAML scenario file"""
        file_path = os.path.abspath(file_path)
        yaml_dict = fameio.load_yaml(file_path, path_resolver)
        scenario = models.Scenario.from_dict(
            definitions=yaml_dict, factory=CustomFameIOFactory()
        )

        # check if layout generation is necessary
        if not _check_all_agents_have_display_coords(scenario):
            logging.info(
                "at least one Agent does not have graph layout coords (X,Y): applying layouting to all agents"
            )
            models.layout_agents(scenario)
        assert _check_all_agents_have_display_coords(scenario)

        return scenario

    @staticmethod
    def save_to_yaml_file(scenario: models.Scenario, file_path: str):
        """Save the given scenario to a YAML file"""
        logging.info("saving scenario to file {}".format(file_path))
        assert os.path.isabs(file_path)

        try:
            with open(file_path, "w") as f:
                yaml.dump(scenario.to_dict(), f)
        except Exception as e:
            raise RuntimeError(
                "failed to save scenario to file '{}'".format(file_path)
            ) from e
