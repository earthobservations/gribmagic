"""Enumerations for remote server types"""
from enum import Enum


class RemoteServerTypes(Enum):
    """Enumeration of remote server types"""
    HTTP = 'http'
    HTTPS = 'https'
    FTP = 'ftps'
    FTPS = 'ftps'
    SFTP = 'sftp'
