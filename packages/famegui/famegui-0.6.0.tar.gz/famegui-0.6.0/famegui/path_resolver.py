import logging
import os
import typing

import fameio.source.path_resolver as fameio
from famegui.appworkingdir import AppWorkingDir


class FameGuiPathResolver(fameio.PathResolver):
    def __init__(self, work_dir: AppWorkingDir):
        self._work_dir = work_dir

    def resolve_yaml_imported_file_pattern(
        self, root_path: str, file_pattern: str
    ) -> typing.List[str]:
        logging.debug(
            "resolving yaml imported file pattern '{}' from root path {}".format(
                file_pattern, root_path
            )
        )
        # first, try to locate the file(s) via the default behaviour
        result = super().resolve_yaml_imported_file_pattern(root_path, file_pattern)
        if len(result) > 0:
            logging.info("resolved yaml imported file(s) to {}".format(result))
            return result

        logging.warning(
            "failed to locate yaml imported file(s) from pattern {}".format(
                file_pattern
            )
        )
        return []

    def resolve_series_file_path(self, file_name: str) -> typing.Optional[str]:
        if os.path.isabs(file_name):
            return file_name

        # try first with the default resolver
        file_path = super().resolve_series_file_path(file_name)
        if file_path:
            return file_path

        # try again in the working dir
        file_path = self._work_dir.find_existing_child_file(file_name)
        if file_path:
            return file_path

        logging.warning("failed to locate timeseries file '{}'".format(file_name))
        return file_path
