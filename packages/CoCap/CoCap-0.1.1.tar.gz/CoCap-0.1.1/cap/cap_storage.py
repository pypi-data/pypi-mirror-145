# -*- coding: utf-8 -*-
import string
from datetime import datetime,timedelta

from numpy import long
from dataclasses import dataclass, field
from pymssql import InternalError
from sqlalchemy import Time, create_engine, exc, Table, MetaData, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.orm import registry

from cap.cap_config import CAPStorageConfig

mapper_registry = registry()


@mapper_registry.mapped
@dataclass
class MessagePublished:
    """
    Published
    """

    __table__ = Table(
        "Published",
        mapper_registry.metadata,
        Column("Id", Integer, primary_key=True, autoincrement=False),
        Column("Version", String, default="V1"),
        Column("Name", String),
        Column("Content", String),
        Column("Retries", Integer, default=0),
        Column("Added", DateTime),
        Column("ExpiresAt", DateTime),
        Column("StatusName", String),
        schema="[cap]"
    )
    Id: int = field(init=False)
    Version: str = None
    Name: str = None
    Content: str = None
    Retries: Integer = None
    Added: DateTime = None
    ExpiresAt: DateTime = None
    StatusName: String = None


class CAPStorageBase(object):
    """
    CAP消息存储基类
    """

    def store_message(self, routing_key, message, status):
        pass


class CAPStorage(CAPStorageBase):
    """
    CAP消息存储
    """

    def __init__(self, config):
        self.config = config

        # 编码特殊字符
        pwd = config['password'].replace("@", "%40")
        self.engine = create_engine(
            'mssql+pymssql://%s:%s@%s/%s' % (config['user'], pwd, config['server'], config['database']))

    def store_message(self, message_id: long, routing_key: string, message: string, status: string):
        """
        存储消息
        """

        try:
            session_cls = sessionmaker(bind=self.engine, autoflush=True)

            with session_cls() as session:

                message_published = MessagePublished()
                message_published.Id = message_id
                message_published.Name = routing_key
                message_published.Content = message
                message_published.Added = str(datetime.now())
                message_published.ExpiresAt = str(datetime.now()+timedelta(days=1))
                message_published.StatusName = status
                session.add(message_published)

                # 提交即保存到数据库:
                session.commit()

        except (exc.InternalError, InternalError):  # 如果创建连接失败，一般意味着数据库本身不可达。此例中是因为目标数据库不存在
            print('连接数据库连接失败')
            raise
