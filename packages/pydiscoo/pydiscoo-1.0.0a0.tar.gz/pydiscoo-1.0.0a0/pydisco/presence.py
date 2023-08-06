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
from typing import Optional

from pydisco.activity import Activity


class ClientStatus:
    """
        This class represents client's status in Discord.

        Attributes
        ----------
        desktop : Optional[str]
            The user's status set for an active desktop (Windows, Linux, Mac) application session.
        mobile : Optional[str]
            The user's status set for an active mobile (iOS, Android) application session.
        web : Optional[str]
            The user's status set for an active web (browser, bot account) application session.
    """

    def __init__(self, data):
        self.desktop: Optional[str] = data.get('desktop')
        self.mobile: Optional[str] = data.get('mobile')
        self.web: Optional[str] = data.get('web')


class Presence:
    """
        This class represents presences in Discord.

        Attributes
        ----------
        id : Optional[int]
            Unique Snowflake ID for this presence.
        user : Optional[User]
            The user presence is being updated for.
        guild_id : Optional[int]
            Id of the guild.
        status : str
            Either "idle", "dnd", "online", or "offline".
        activities : Optional[Activity]
            User's current activities.
        client_status : Optional[ClientStatus]
            User's platform-dependent status.
    """

    def __init__(self, data, http):
        if data.get('id') is not None:
            self.id: Optional[int] = int(data.get('id'))
        if data.get('user') is not None:
            self.user: Optional[int] = int(data.get('user').get('id'))
        if data.get('guild_id') is not None:
            self.guild_id: Optional[int] = int(data.get('guild_id'))
        self.status: Optional[str] = data.get('status')
        if data.get('activities') is not None:
            self.activities: Optional[list[Activity]] = [
                Activity(x, http) for x in data.get('activities')]
        if data.get('client_status') is not None:
            self.client_status: Optional[ClientStatus] = data.get('client_status')
