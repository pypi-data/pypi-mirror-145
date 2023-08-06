# -*- coding: utf-8 -*-

import string


class CAPStorageConfig(object):
    """
    CAP持久化配置
    """

    def __init__(self, server: string, database: string, user: string,
                 password: string):
        self.server = server
        self.database = database
        self.user = user
        self.password = password


class CAPConfig(object):
    """
    CAP配置
    """

    def __init__(self, host: string, port: string, virtual_host: string, exchange: string, user: string,
                 password: string, storage: CAPStorageConfig):
        self.host = host
        self.port = port
        self.virtual_host = virtual_host
        self.exchange = exchange
        self.user = user
        self.password = password
        self.storage: CAPStorageConfig = storage
