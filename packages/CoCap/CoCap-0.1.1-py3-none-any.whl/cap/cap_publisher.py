# -*- coding: utf-8 -*-

import json
import pika
import time

from cap.cap_config import CAPConfig, CAPStorageConfig
from cap.cap_storage import CAPStorage


class CAPPublisher(object):
    """
    CAP消息发布器
    """

    def __init__(self, config):
        self.config = config

    def publish(self, routing_key, message):
        """
        发布消息
        """

        try:

            credentials = pika.PlainCredentials(self.config['user'], self.config['password'])  # mq用户名和密码
            with pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.config['host'], port=self.config['port'],
                                              virtual_host=self.config['virtual_host'],
                                              credentials=credentials)) as connection:
                message_bytes = bytes(json.dumps(message), encoding="utf8")
                message_id = time.time_ns()
                sent_time = time.strftime("%m/%d/%Y %H:%M:%S +08:00", time.localtime())
                message_headers = {
                    "cap-msg-id": "%s" %message_id,
                    "cap-corr-id": "%s" %message_id,
                    "cap-corr-seq": "0",
                    "cap-msg-name": routing_key,
                    "cap-msg-type": "object",
                    "cap-senttime": sent_time
                }

                # 向队列插入数值 routing_key是队列名
                channel = connection.channel()
                channel.basic_publish(exchange=self.config['exchange'],
                                      routing_key=routing_key,
                                      body=message_bytes,
                                      properties=pika.BasicProperties(delivery_mode=2, headers=message_headers))

                storage_message = {
                    "Headers": message_headers,
                    "Value": message
                }
                self.__store_message(message_id, routing_key, json.dumps(storage_message), "Succeeded")
        except:
            self.__store_message(message_id, routing_key, json.dumps(storage_message), "Failed")
            raise

    def __store_message(self, message_id, routing_key, message, status):
        """
        存储消息
        """
        storage = CAPStorage(self.config['storage'])
        storage.store_message(message_id, routing_key, message, status)


if __name__ == '__main__':
    config = {
        "host": "rabbitmq.dev.co",
        "port": "15672",
        "enabled": "true",
        "virtual_host": "CityOcean-Test",
        "exchange": "CO-Exchange",
        "user": "co",
        "password": "co@rabbitmq.com",
        "storage": {
            "server": "db.test.com",
            "database": "CO_EventBus",
            "user": "co",
            "password": "Co&23@2332$22"
        }
    }
    publisher = CAPPublisher(config)
    publisher.publish("spider_container_tracking_changed3", ["MRKU2226829", "MSKU8479446"])
