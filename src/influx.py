from config import Config
from datetime import datetime, timezone
from loguru import self.logger
from influxdb import InfluxDBClient


class InfluxClient(Config):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8086,
        database: str = "measurements",
        username: str = "",
        password: str = "",
    ):
        super().__init__()
        self.influx = InfluxDBClient(
            host=host,
            port=port,
            username=username,
            password=password,
            database=database,
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