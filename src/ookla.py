from config import Config
from speedtest import Speedtest
from statistics import mean


class OoklaClient(Config):
    def __init__(self):
        super().__init__()
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
            self.logger.debug(f"Measuring download bandwith, sample {index + 1}")
            bits = self._ookla.download()
            megabits.append(bits / 1000000)

        average_megabits = round(mean(megabits), 2)
        self.logger.debug(f"measurements: {megabits}")
        self.logger.info(
            f"Download bandwith mean of {samples} measurements: {average_megabits}"
        )
        return average_megabits

    def measure_upload(self, samples: int = 3, share: bool = False):
        megabits = []
        for index, sample in enumerate(range(samples)):
            self.logger.debug(f"Measuring upload bandwith, sample {index}")
            bits = self._ookla.upload()
            megabits.append(bits / 1000000)

        average_megabits = round(mean(megabits), 2)
        self.logger.debug(f"measurements: {megabits}")
        self.logger.info(
            f"Upload bandwith mean of {samples} measurements: {average_megabits}"
        )
        return average_megabits

    def get_config(self):
        return self._ookla.get_config()


if __name__ == "__main__":
    x = OoklaClient()
    print(x.measure_download())
    print(x.measure_upload())
    print(x.get_config())
