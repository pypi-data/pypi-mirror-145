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
from typing import Optional, Union, Any

from pydisco.utils import Snowflake


class Role(Snowflake):
    """
        This class represents roles in Discord.

        Attributes
        ----------
        id : int
            Unique Snowflake ID for this role.
        name : str
            The name of this role.
        color: int
            Hexadecimal value for color of this role.
        hoist : bool
            Displays whether the display of participants with this role is enabled separately?
        icon: str, any, optional
            The icon for this role.
        unicode_emoji : str
            Unicode emoji for this role.
        position : int
            The position of this role on the list.
        permissions : str
            Permissions bit.
        managed : bool
            Determines whether this role belongs to one of the server's integrations (e.g., bot).
        mentionable : bool
            Determines whether a given role can be mentioned in the text channel.
    """

    def __init__(self, data):
        self.id: int = int(data.get('id'))
        super().__init__(self.id)
        self.name: str = data.get('name')
        self.color: int = int(data.get('color'))  # TODO: custom color class
        self.hoist: bool = data.get('hoist')
        self.icon: Optional[Union[str, Any]] = data.get('icon')
        self.unicode_emoji: Optional[Union[str, Any]] = data.get('unicode_emoji')
        self.position: int = int(data.get('position'))
        self.permissions: int = int(data.get('permissions'))
        self.managed: bool = data.get('managed')
        self.mentionable: bool = data.get('mentionable')

    def __repr__(self) -> str:
        return f'@{self.name} ({self.id})'
