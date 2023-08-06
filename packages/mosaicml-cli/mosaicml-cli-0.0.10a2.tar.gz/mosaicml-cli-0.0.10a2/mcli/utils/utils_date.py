"""This Module stores utils for pretty printing Datetime objects"""
from datetime import datetime


def time_since(date: datetime) -> str:
    seconds = (datetime.now() - date).total_seconds()
    interval = seconds / 31536000
    if interval > 1:
        return f'{int(interval)} years'
    interval = seconds / 2592000
    if interval > 1:
        return f'{int(interval)} months'
    interval = seconds / 86400
    if interval > 1:
        return f'{int(interval)} days'
    interval = seconds / 3600
    if interval > 1:
        return f'{int(interval)} hours'
    interval = seconds / 60
    if interval > 1:
        return f'{int(interval)} minutes'

    return f'{int(interval)} seconds'
