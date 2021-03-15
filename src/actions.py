from config import Configurator


class Actions(Configurator):
    def __init__(self):
        super().__init__()
        if self.DATABASE_ENABLED:
            self.database = self.get_database_client()
        if self.SPEEDTEST_ENABLED:
            self.speedtest = self.get_speedtest_client()
        if self.MODEM_ENABLED:
            self.modem = self.get_modem_client()

        self.isp = self.speedtest.get_isp()
        self.ip = self.speedtest.get_ip()
        self.country = self.speedtest.get_country()
        self.cell_id = self.modem.get_cell_id()

    def measure_signal(self):
        pass
        # self.rsrq = self.modem.get_rsrq()
        # self.rsrp = self.modem.get_rsrp()
        # self.rssi = self.modem.get_rssi()

    def measure_download(self):
        tags = {
            "measurement": "download",
            "isp": self.isp,
            "ip": self.ip,
            "country": self.country,
            "cell_id": self.cell_id,
        }
        data = {
            "pre_download_traffic": self.modem.get_download_traffic(),
            "download_bandwith": self.speedtest.measure_download(),
            "isp": self.isp,
            "ip": self.ip,
            "cell_id": self.cell_id,
        }
        self.logger.info(data)
        self.database.post(measurement="download_bandwith", data=data, tags=tags)

    def measure_upload(self):
        tags = {
            "measurement": "upload",
            "isp": self.isp,
            "ip": self.ip,
            "country": self.country,
            "cell_id": self.cell_id,
        }
        data = {
            "pre_upload_traffic": self.modem.get_upload_traffic(),
            "upload_bandwidth": self.speedtest.measure_upload(),
            "isp": self.isp,
            "ip": self.ip,
            "cell_id": self.cell_id,
        }
        self.logger.info(data)
        self.database.post(measurement="upload_bandwith", data=data, tags=tags)


if __name__ == "__main__":
    x = Actions()
    x.measure_download()
    x.measure_upload()