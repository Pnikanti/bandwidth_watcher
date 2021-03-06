from config import Config
from datetime import datetime, timezone
from influxdb import InfluxDBClient


class InfluxClient(Config):
    def __init__(self):
        super().__init__()
        self._username = self.get("Influx", "username")
        self._password = self.get("Influx", "password")
        self._address = self.get("Influx", "address")
        self._port = self.get("Influx", "port")
        self._database = self.get("Influx", "database")

        self.influx = InfluxDBClient(
            host=self._address,
            port=self._port,
            username=self._username,
            password=self._password,
            database=self._database,
        )

    def _parse_nested_dictionaries(
        self,
        data: dict,
        new_data: dict = {},
        recursive_key: str = "",
        recursive: bool = False,
    ):
        for (key, value) in data.items():
            # if iterated value is a dict, recursively call this function
            if isinstance(value, dict):
                self._parse_nested_dictionaries(
                    value, new_data=new_data, recursive_key=key, recursive=True
                )
            # if recursive and iterated value is not dict
            elif recursive and not isinstance(value, dict):
                new_key = f"{recursive_key}-{key}".replace(" ", "_").lower()
                new_data[new_key] = value
            # if iterated value is not dict or recursive
            else:
                new_key = key.replace(" ", "_").lower()
                new_data[new_key] = value

        return new_data

    def query(self, query: str):
        result = self.influx.query(query)
        self.logger.info(f"Query returned: {result}")
        return query

    def post(self, measurement: str, data: dict, tags: dict, debug: bool = False):
        data = self._parse_nested_dictionaries(data)
        utcnow = f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%I:%S.%f')[:-3]}Z"
        body = [
            {
                "measurement": measurement,
                "tags": tags,
                "time": utcnow,
                "fields": data,
            }
        ]
        self.logger.info(f"Posting: {body}")
        self.influx.write_points(body)


if __name__ == "__main__":
    x = InfluxClient()