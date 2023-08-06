# Press the green button in the gutter to run the script.
import pytest

from cap.cap_config import CAPConfig, CAPStorageConfig
from cap.cap_publisher import CAPPublisher


class TestCap:
    def setup(self):
        host = 'rabbitmq.dev.co'
        port = '15672'
        virtual_host = 'CityOcean-Dev'
        exchange = 'CO-Exchange'
        user = 'co'
        password = 'co@rabbitmq.com'
        storage_server = 'db.dev.com'
        storage_database = 'CO_EventBus'
        storage_user = 'co'
        storage_password = 'Co&23@2332$22'
        print('初始化客户端')
        config: CAPConfig = CAPConfig(host=host, port=port, virtual_host=virtual_host,
                                      exchange=exchange, user=user, password=password,
                                      storage=CAPStorageConfig(server=storage_server, database=storage_database,
                                                               user=storage_user,
                                                               password=storage_password))
        self.publisher = CAPPublisher(config)

    def teardown(self):
        print('关闭客户端')

    def test_publish(self):
        self.publisher.publish("spider_container_tracking_changed", ["MRKU2226829", "MSKU8479446"])


if __name__ == '__main__':
    pytest.main("-q --html=report.html")
