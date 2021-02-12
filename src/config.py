import json
import sys
from loguru import logger
from functools import reduce


class Config:
    def __init__(self):
        self.logger = logger
        # get callee filename without extension
        self._callee = (
            sys._getframe()
            .f_back.f_code.co_filename.replace("\\", "/")
            .split("/")[-1]
            .replace(".py", "")
        )
        self._configfile = "../configs/configuration.json"
        self._configuration = self._get_configuration()
        self._logging_settings = self._configuration["Ecosystem"]["Logging"]
        self._logfile = f"./logs/{self._callee}.log"
        self._loggers = self._set_loggers()

    def _set_loggers(self):
        sinks = []
        # remove inital logger
        self.logger.remove()

        sinks.append(
            self.logger.add(
                sys.stdout, level=self._logging_settings.get("loglevel", "INFO")
            )
        )
        if self._logging_settings.get("log-to-file", False):
            sinks.append(
                self.logger.add(
                    self._logfile, level=self._logging_settings.get("loglevel", "INFO")
                )
            )

        return sinks

    def _del_loggers(self):
        if self._loggers:
            for id in self._loggers:
                self.logger.remove(id)

    def _get_configuration(self):
        with open(self._configfile, "r") as file:
            return json.load(file)

    def get(self, *args):
        return reduce(
            lambda d, key: d.get(key, None) if isinstance(d, dict) else None,
            args,
            self._configuration,
        )


if __name__ == "__main__":
    x = Config()
    print(x._callee)