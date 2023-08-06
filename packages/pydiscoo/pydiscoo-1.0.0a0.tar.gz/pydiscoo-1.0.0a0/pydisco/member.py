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
from typing import Optional, Union, Any

from pydisco.user import User
from pydisco.utils import convert_iso_timestamp


class Member:
    def __init__(self, data, _http):
        if data.get('user') is not None:
            self.user: Optional[User] = User(data.get('user'), _http)
        self.nick: Optional[Union[str, Any]] = data.get('nick')
        self.avatar: Optional[Union[str, Any]] = data.get('avatar')
        self.roles: list[int] = data.get('roles')
        self.joined_at: datetime = convert_iso_timestamp(data.get('joined_at'))
        if data.get('premium_since') is not None:
            self.premium_since: Optional[datetime] = convert_iso_timestamp(data.get('premium_since'))
        self.deaf: bool = data.get('deaf')
        self.mute: bool = data.get('mute')
        self.pending: Optional[bool] = data.get('pending')
        self.permissions: Optional[str] = data.get('permissions')
        if data.get('communication_disabled_until') is not None:
            self.communication_disabled_until: Optional[datetime] = convert_iso_timestamp(
                data.get('communication_disabled_until'))
