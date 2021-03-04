import sys
import os
import json
import yaml
from loguru import logger
from functools import reduce


class Config:
    def __init__(self, config_file: str = "configuration.yaml"):
        self.logger = logger
        self._config_file = config_file
        self._config_file_extension = self._config_file.split(".")[-1]
        self._config_folder = "configs"

        # get callee filename without extension
        self._callee = (
            sys._getframe()
            .f_back.f_code.co_filename.replace("\\", "/")
            .split("/")[-1]
            .replace(".py", "")
        )
        # get absolute path to current __file__
        self._abs_path_to_current_file = (
            os.path.realpath(__file__).replace("\\", "/").split("/")
        )[1:]
        # get absolute path to parent folder
        self._abs_path_to_parent_folder = os.path.join(
            os.sep,
            *self._abs_path_to_current_file[
                0 : self._abs_path_to_current_file.index("src")
            ],
        )
        # get absolute path to configuration file
        self._abs_path_to_config_file = os.path.join(
            self._abs_path_to_parent_folder, self._config_folder, self._config_file
        )

        if (
            self._config_file_extension == "yaml"
            or self._config_file_extension == "yml"
        ):
            self._configuration = self._get_yaml_configuration(
                self._abs_path_to_config_file
            )
        elif self._config_file_extension == "json":
            self._configuration = self._get_json_configuration(
                self._abs_path_to_config_file
            )

        assert self._configuration, "Configuration was not set. Aborting!"

        self._logging_settings = self._configuration["LOGGING"]
        self._logfile = f"./logs/{self._callee}.log"
        self._loggers = self._set_loggers()

    def _set_loggers(self):
        sinks = []
        # remove inital logger
        self.logger.remove()

        sinks.append(
            self.logger.add(
                sys.stdout, level=self._logging_settings.get("LOGLEVEL", "INFO")
            )
        )
        if self._logging_settings.get("TOFILE", False):
            sinks.append(
                self.logger.add(
                    self._logfile, level=self._logging_settings.get("LOGLEVEL", "INFO")
                )
            )

        return sinks

    def _del_loggers(self):
        if self._loggers:
            for id in self._loggers:
                self.logger.remove(id)

    def _get_yaml_configuration(self, input_file: str):
        try:
            with open(input_file, "r") as file:
                return yaml.safe_load(file)
        except (FileNotFoundError, yaml.YAMLError) as err:
            raise AssertionError(
                f"Could not load the configuration file: '{input_file}'!"
            ) from err

    def _get_json_configuration(self, input_file: str):
        try:
            with open(input_file, "r") as file:
                return json.load(file)
        except FileNotFoundError as err:
            raise AssertionError(
                f"Could not load the configuration file: '{input_file}'!"
            ) from err

    def get(self, *args):
        return reduce(
            lambda d, key: d.get(key, None) if isinstance(d, dict) else None,
            args,
            self._configuration,
        )


if __name__ == "__main__":
    x = Config()
    print(x._callee)