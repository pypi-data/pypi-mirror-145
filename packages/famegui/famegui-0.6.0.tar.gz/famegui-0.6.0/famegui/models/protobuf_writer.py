import logging
import os

import fameio.source as fameio
import famegui.models as models


def write_protobuf_output(
    scenario: models.Scenario, output_path: str, path_resolver: fameio.PathResolver
) -> None:
    logging.debug("generating protobuf output to '{}'".format(output_path))
    assert os.path.isabs(output_path)

    fameio.SchemaValidator.ensure_is_valid_scenario(scenario)
    writer = fameio.ProtoWriter(output_path, path_resolver)
    writer.write_validated_scenario(scenario)
    logging.info("protobuf output was generated to '{}'".format(output_path))
