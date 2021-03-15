from config import Core
from statistics import mean


class Speedtester(Core):
    def __init__(self):
        super().__init__()


class OoklaClient(Speedtester):
    def __init__(self):
        super().__init__()
        self._ookla = Speedtest()
        self.config = self._ookla.get_config()

    def get_isp(self):
        return self.config["client"]["isp"]

    def get_ip(self):
        return self.config["client"]["ip"]

    def get_country(self):
        return self.config["client"]["country"]

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
            self.logger.debug(f"Measuring upload bandwith, sample {index + 1}")
            bits = self._ookla.upload()
            megabits.append(bits / 1000000)

        average_megabits = round(mean(megabits), 2)
        self.logger.debug(f"measurements: {megabits}")
        self.logger.info(
            f"Upload bandwith mean of {samples} measurements: {average_megabits}"
        )
        return average_megabits


if __name__ == "__main__":
    x = OoklaClient()
    print(x.measure_download())
    print(x.measure_upload())