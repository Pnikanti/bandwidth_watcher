from config import Config
from influx import InfluxClient
from ookla import OoklaClient


class Actions(Config):
    def __init__(self):
        super().__init__()
        self.influx = InfluxClient()
        self.ookla = OoklaClient()

    def measure_download(self):
        data = {}
        settings = self.ookla.get_config()
        tags = {
            "measurement": "download",
            "isp": settings["client"]["isp"],
            "ip": settings["client"]["ip"],
            "country": settings["client"]["country"],
        }
        data["download_bandwith"] = self.ookla.measure_download()
        self.influx.post(measurement="download_bandwith", data=data, tags=tags)

    def measure_upload(self):
        data = {}
        settings = self.ookla.get_config()
        tags = {
            "measurement": "upload",
            "isp": settings["client"]["isp"],
            "ip": settings["client"]["ip"],
            "country": settings["client"]["country"],
        }
        data["upload_bandwith"] = self.ookla.measure_upload()
        self.influx.post(measurement="upload_bandwith", data=data, tags=tags)


if __name__ == "__main__":
    x = Actions()
    x.measure_download()
    x.measure_upload()