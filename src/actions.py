from config import Config
from modem import HuaweiClient
from influx import InfluxClient
from ookla import OoklaClient


class Actions(Config):
    def __init__(self):
        super().__init__()
        self.huawei = HuaweiClient()
        self.influx = InfluxClient()
        self.ookla = OoklaClient()
        self.isp = self.ookla.get_isp()
        self.ip = self.ookla.get_ip()
        self.country = self.ookla.get_country()
        self.cell_id = self.huawei.get_cell_id()
        self.rsrq = self.huawei.get_rsrq()
        self.rsrp = self.huawei.get_rsrp()
        self.rssi = self.huawei.get_rssi()

    def measure_download(self):
        tags = {
            "measurement": "download",
            "isp": self.isp,
            "ip": self.ip,
            "country": self.country,
            "cell_id": self.cell_id,
        }
        data = {
            "pre_download_traffic": self.huawei.get_download_traffic(),
            "download_bandwith": self.ookla.measure_download(),
            "isp": self.isp,
            "ip": self.ip,
            "cell_id": self.cell_id,
            "rsrq": self.rsrq,
            "rsrp": self.rsrp,
            "rssi": self.rssi,
        }
        self.logger.info(data)
        self.influx.post(measurement="download_bandwith", data=data, tags=tags)

    def measure_upload(self):
        tags = {
            "measurement": "upload",
            "isp": self.isp,
            "ip": self.ip,
            "country": self.country,
            "cell_id": self.cell_id,
        }
        data = {
            "pre_upload_traffic": self.huawei.get_download_traffic(),
            "download_bandwith": self.ookla.measure_download(),
            "isp": self.isp,
            "ip": self.ip,
            "cell_id": self.cell_id,
            "rsrq": self.rsrq,
            "rsrp": self.rsrp,
            "rssi": self.rssi,
        }
        self.logger.info(data)
        self.influx.post(measurement="upload_bandwith", data=data, tags=tags)


if __name__ == "__main__":
    x = Actions()
    x.measure_download()
    x.measure_upload()