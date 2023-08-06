#!/usr/bin/python
# -*- coding: utf-8 -*-
# cython: language_level=3
"""
MIT License

Copyright (c) 2021-present, Pelfox.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from datetime import datetime

DISCORD_EPOCH = 1420070400000


def convert_snowflake_to_datetime(snowflake: int) -> datetime:
    """Method to convert Snowflake ID to the :class:`datetime`.

    Parameters
    ----------
    snowflake : int
        Snowflake ID to convert.

    Returns
    -------
    :class:`datetime`
        Converted result.
    """
    timestamp = ((snowflake >> 22) + DISCORD_EPOCH) / 1000
    return datetime.utcfromtimestamp(timestamp)


def convert_iso_timestamp(timestamp: str) -> datetime:
    """Convert ISO8601 timestamp into :class:`datetime`.

    Parameters
    ----------
    timestamp : str
        Inputted ISO8601 timestamp.

    Returns
    -------
    :class:`datetime`
        Converted timestamp.
    """
    return datetime.fromisoformat(timestamp)


def convert_timestamp(timestamp: int) -> datetime:
    """Convert UNIX timestamp into :class:`datetime`.

    Parameters
    ----------
    timestamp : int
        Timestamp to convert.

    Returns
    -------
    :class:`datetime`
        Converted timestamp.
    """
    return datetime.utcfromtimestamp(timestamp)


class Snowflake:
    """
        This class represents another class, that contains snowflakes values.

        Attributes
        ----------
        id : int
            Unique Snowflake ID for this class.

        Methods
        -------
        created_at : :class:`datetime`
            Converts class' ID to :class:`datetime` instance.
    """

    def __init__(self, id: int):
        self.id: int = id

    def created_at(self) -> datetime:
        """:class:`datetime` Instance of datetime class, that represents when id was created."""
        return convert_snowflake_to_datetime(self.id)

    def __repr__(self) -> str:
        return f'Snowflake[id={self.id}]'
