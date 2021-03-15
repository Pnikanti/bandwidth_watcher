import re
from config import Core
from statistics import mean


class Modem(Core):
    def __init__(self):
        super().__init__()
        try:
            self._username = os.environ["ROUTER_USERNAME"]
            self._password = os.environ["ROUTER_PASSWORD"]
        except KeyError as err:
            raise AssertionError(
                'Router credentials not set! Please set "ROUTER_USERNAME" and "ROUTER_PASSWORD" environment variables.'
            ) from err


class HuaweiClient(Modem):
    def __init__(self):
        super().__init__()
        try:
            from huawei_lte_api.Client import Client, Monitoring
            from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
        except ImportError as err:
            raise AssertionError(f"Could not find HuaweiClient module!") from err

        self._address = self.get("Modem", "address")
        self._connection = AuthorizedConnection(
            f"http://{self._username}:{self._password}@{self._address}/"
        )
        self._client = Client(self._connection)
        self.signal = self._client.device.signal()
        self.information = self._client.device.information()

    def get_signal_raw(self):
        signal_raw = self.signal
        self.logger.info(f"Signal information: {signal_raw}")
        return signal_raw

    def get_cell_id(self):
        cell_id = self.signal["cell_id"]
        self.logger.info(f"Cell ID: {cell_id}")
        return int(re.sub(r"\D", "", cell_id))

    def get_rssi(self):
        rssi = self.signal["rssi"]
        self.logger.info(f"RSSI: {rssi}")
        return int(re.sub(r"\D", "", rssi))

    def get_rsrp(self):
        rsrp = self.signal["rsrp"]
        self.logger.info(f"RSRP: {rsrp}")
        return int(re.sub(r"\D", "", rsrp))

    def get_rsrq(self):
        rsrq = self.signal["rsrq"]
        self.logger.info(f"RSRQ: {rsrq}")
        return int(re.sub(r"\D", "", rsrq))

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