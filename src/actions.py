from config import Config
from huawei import HuaweiClient
from influx import InfluxClient
from ookla import OoklaClient


class Actions(Config):
    def __init__(self):
        super().__init__()
        self.huawei = HuaweiClient()
        self.influx = InfluxClient()
        self.ookla = OoklaClient()
        self.settings = self.ookla.get_config()

    def measure_download(self):
        data = {}
        signal = self.huawei.get_signal()
        tags = {
            "measurement": "download",
            "isp": self.settings["client"]["isp"],
            "ip": self.settings["client"]["ip"],
            "country": self.settings["client"]["country"],
            "cell_id": signal["cell_id"],
        }
        data["pre_download_traffic"] = self.huawei.get_download_traffic()
        data["download_bandwith"] = self.ookla.measure_download()
        data["isp"] = self.settings["client"]["isp"]
        data["ip"] = self.settings["client"]["ip"]
        data["cell_id"] = signal["cell_id"]
        data["rsrq"] = signal["rsrq"]
        data["rsrp"] = signal["rsrp"]
        data["rssi"] = signal["rssi"]
        self.logger.info(data)
        self.influx.post(measurement="download_bandwith", data=data, tags=tags)

    def measure_upload(self):
        data = {}
        signal = self.huawei.get_signal()
        tags = {
            "measurement": "upload",
            "isp": self.settings["client"]["isp"],
            "ip": self.settings["client"]["ip"],
            "country": self.settings["client"]["country"],
            "cell_id": signal["cell_id"],
        }
        data["pre_upload_traffic"] = self.huawei.get_upload_traffic()
        data["upload_bandwith"] = self.ookla.measure_upload()
        data["isp"] = self.settings["client"]["isp"]
        data["ip"] = self.settings["client"]["ip"]
        data["cell_id"] = signal["cell_id"]
        data["rsrq"] = signal["rsrq"]
        data["rsrp"] = signal["rsrp"]
        data["rssi"] = signal["rssi"]
        self.logger.info(data)
        self.influx.post(measurement="upload_bandwith", data=data, tags=tags)


if __name__ == "__main__":
    x = Actions()
    x.measure_download()
    x.measure_upload()