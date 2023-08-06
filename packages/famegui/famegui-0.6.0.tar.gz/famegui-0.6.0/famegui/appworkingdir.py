import os
import logging
import typing


class AppWorkingDir:
    """Class used to find and access the files from the FAME GUI working directory"""

    _SCHEMAS_DIR_NAME = "schemas"
    _SCENARIOS_DIR_NAME = "scenarios"
    _TIMESERIES_DIR_NAME = "timeseries"
    _PROTOBUF_DIR_NAME = "protobuf"

    def __init__(self, root_dir: str):
        self._root_dir = os.path.abspath(root_dir).replace("\\", "/")

    @property
    def root_dir(self) -> str:
        return self._root_dir

    @property
    def schemas_dir(self):
        return os.path.join(self._root_dir, self._SCHEMAS_DIR_NAME)

    @property
    def scenarios_dir(self):
        return os.path.join(self._root_dir, self._SCENARIOS_DIR_NAME)

    @property
    def timeseries_dir(self):
        return os.path.join(self._root_dir, self._TIMESERIES_DIR_NAME)

    @property
    def protobuf_dir(self):
        return os.path.join(self._root_dir, self._PROTOBUF_DIR_NAME)

    def make_relative_path(self, file_path: str) -> str:
        result = os.path.abspath(file_path).replace("\\", "/")
        if result.startswith(self.root_dir):
            result = "." + result[len(self.root_dir) :]
        return result

    def make_full_path(self, path: str) -> str:
        if os.path.isabs(path):
            return path.replace("\\", "/")
        result = os.path.join(self._root_dir, path)
        return os.path.abspath(result).replace("\\", "/")

    def find_existing_child_file(self, path: str) -> typing.Optional[str]:
        abs_path = self.make_full_path(path)
        if os.path.isfile(abs_path):
            return abs_path
        logging.info(
            "failed to locate child path '{}' in working directory".format(path)
        )
        # review: Why do we need an explicit return None at this point? Could we not just remove it without
        #  any consequences? Also why do we not return a str instance as declared in the typehint? Is this
        #  a signal to the above application layer?
        return None

    def list_existing_schema_files(self) -> typing.List[str]:
        logging.debug("listing yaml files in {}".format(self.schemas_dir))
        result = []
        for filename in os.listdir(self.schemas_dir):
            if filename.endswith(".yaml"):
                # always return a relative path in UNIX style
                result.append("./{}/{}".format(self._SCHEMAS_DIR_NAME, filename))
            else:
                logging.warning(
                    "ignoring file '{}' in {}".format(filename, self.schemas_dir)
                )
        return result
