import sys
import os
from loguru import logger
from speedtest import Speedtest
from statistics import mean

logger.add(sys.stdout, level=os.environ.get("LOGLEVEL", "INFO"))
logger.add(
    "./logs/run.log",
    retention="14 days",
    level=os.environ.get("LOGLEVEL", "INFO"),
)


class OoklaWrapper:
    def __init__(self):
        self._ookla = Speedtest()
        self._ookla.get_best_server()

    def get_closest_server(self):
        return self._ookla.get_closest_servers()

    def get_best_server(self):
        return self._ookla.get_best_server()

    def change_server(self, server: str):
        return self._ookla.set_mini_server(server)

    def measure_download(self, samples: int = 3, share: bool = False):
        megabits = []
        for index, sample in enumerate(range(samples)):
            logger.debug(f"Measuring download bandwith, sample {index + 1}")
            bits = self._ookla.download()
            megabits.append(bits / 1000000)

        average_megabits = round(mean(megabits), 2)
        logger.debug(f"measurements: {megabits}")
        logger.info(
            f"Download bandwith mean of {samples} measurements: {average_megabits}"
        )
        return average_megabits

    def measure_upload(self, samples: int = 3, share: bool = False):
        megabits = []
        for index, sample in enumerate(range(samples)):
            logger.debug(f"Measuring upload bandwith, sample {index}")
            bits = self._ookla.upload()
            megabits.append(bits / 1000000)

        average_megabits = round(mean(megabits), 2)
        logger.debug(f"measurements: {megabits}")
        logger.info(
            f"Upload bandwith mean of {samples} measurements: {average_megabits}"
        )
        return average_megabits

    def get_config(self):
        return self._ookla.get_config()


if __name__ == "__main__":
    x = OoklaWrapper()
    print(x.measure_download())
    print(x.measure_upload())
    print(x.get_config())
