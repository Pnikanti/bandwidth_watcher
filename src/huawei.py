from config import Config
from statistics import mean
from huawei_lte_api.Client import Client, Monitoring
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection


class HuaweiClient(Config):
    def __init__(self):
        super().__init__()
        self._username = self.get("Modem", "username")
        self._password = self.get("Modem", "password")
        self._url = self.get("Modem", "url")
        self._connection = AuthorizedConnection(
            f"http://{self._username}:{self._password}@{self._url}/"
        )
        self._client = Client(self._connection)

    def get_signal(self):
        signal = self._client.device.signal()
        self.logger.info(signal)
        return signal

    def get_information(self):
        information = self._client.information()
        config.logger.info(information)
        return information

    def get_connected_devices(self):

    def get_download_traffic(self, samples: int = 10):
        megabits = []
        for sample in range(samples):
            download_rate_bits = (
                int(self._client.monitoring.traffic_statistics()["CurrentDownloadRate"])
                * 8
            )
            megabits.append(download_rate_bits / 1000000)
        average_megabits = round(mean(megabits), 2)
        self.logger.info(f"Average download rates (bits): {average_megabits}")
        return average_megabits

    def get_upload_traffic(self, samples: int = 10):
        megabits = []
        for sample in range(samples):
            upload_rate_bits = (
                int(self._client.monitoring.traffic_statistics()["CurrentUploadRate"])
                * 8
            )
            megabits.append(upload_rate_bits / 1000000)
        average_megabits = round(mean(megabits), 2)
        self.logger.info(f"Average upload rates (bits): {average_megabits}")
        return average_megabits


if __name__ == "__main__":
    x = HuaweiClient()
    print(x.get_signal())
    print(x.get_download_traffic())
    print(x.get_upload_traffic())