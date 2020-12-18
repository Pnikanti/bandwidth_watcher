import sys
import os
from loguru import logger
from influxwrapper import InfluxWrapper
from ooklawrapper import OoklaWrapper

logger.add(sys.stdout, level=os.environ.get("LOGLEVEL", "INFO"))
logger.add(
    "./logs/run.log",
    retention="14 days",
    level=os.environ.get("LOGLEVEL", "INFO"),
)


class Actions:
    def __init__(self):
        self.influx = InfluxWrapper()
        self.ookla = OoklaWrapper()

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