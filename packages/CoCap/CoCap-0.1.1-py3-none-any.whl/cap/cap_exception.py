# -*- coding: utf-8 -*-


class CAPException(Exception):
    """
    CAP异常
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
