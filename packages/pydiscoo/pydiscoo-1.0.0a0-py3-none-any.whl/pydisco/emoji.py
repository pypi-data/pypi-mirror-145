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
from typing import Union, Optional, Any

from pydisco.user import User
from pydisco.utils import Snowflake


class Emoji(Snowflake):
    """
        This class represents emojis in Discord.

        Attributes
        ----------
        id : int
            Unique Snowflake ID for this emoji.
        name : str
            The name of this emoji.
        require_colons : bool, optional
            Does this emoji need to be wrapped in a colon (for example, :shy:).
        managed : bool, optional
            Can this emoji be managed?
        animated : bool, optional
            Is this emoji animated?
        available : bool, optional
            Can a bot access this emoji?

        Methods
        -------
        roles : list[:class:`Role`]
            A list of roles that can use this emoji.
        user : :class:`User`, optional
            The user that created this emoji.
        created_at : :class:`datetime`
            When this emoji was created.
    """

    def __init__(self, data, http):
        if data.get('id') is None:
            self.id: int = None  # type: ignore
        else:
            self.id: int = int(data.get('id'))
        super().__init__(self.id)
        self.name: Union[str, Any] = data.get('name')
        self.require_colons: Optional[bool] = data.get('require_colons')
        self.managed: Optional[bool] = data.get('managed')
        self.animated: Optional[bool] = data.get('animated')
        self.available: Optional[bool] = data.get('available')
        if data.get('roles') is not None:
            self.roles: list[int] = list(map(int, data.get('roles')))
        if data.get('user') is not None:
            self.user: User = User(data.get('user'), http)  # TODO: maybe use caching for users?

    def __repr__(self) -> str:
        return f'{self.name} ({self.id})'
