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
from typing import Optional, Any, Union

from pydisco.member import Member
from pydisco.utils import convert_iso_timestamp


class VoiceState:
    """
        This class represents Voice States in Discord.

        Attributes
        ----------
        guild_id : Optional[int]
            The guild id this voice state is for.
        channel_id : Union[int, Any]
            The channel id this user is connected to.
        user_id : int
            The user id this voice state is for.
        member : Optional[Member]
            The guild member this voice state is for.
        session_id : str
            The session id for this voice state.
        deaf : bool
            Whether this user is deafened by the server.
        mute : bool
            Whether this user is muted by the server.
        self_deaf : bool
            Whether this user is locally deafened.
        self_mute : bool
            Whether this user is locally muted.
        self_stream : Optional[bool]
            Whether this user is streaming using "Go Live".
        self_video : bool
            Whether this user's camera is enabled.
        suppress : bool
            Whether this user is muted by the current user.
        request_to_speak_timestamp : datetime
            The time at which the user requested to speak.
    """

    def __init__(self, data, http):
        self.guild_id: Optional[int] = data.get('guild_id')
        self.channel_id: Union[int, Any] = data.get('channel_id')
        self.user_id: int = data.get('user_id')
        if data.get('member') is not None:
            self.member: Optional[Member] = Member(data.get('member'), http)
        self.session_id: str = data.get('session_id')
        self.deaf: bool = data.get('deaf')
        self.mute: bool = data.get('mute')
        self.self_deaf: bool = data.get('self_deaf')
        self.self_mute: bool = data.get('self_mute')
        self.self_stream: Optional[bool] = data.get('self_stream')
        self.self_video: bool = data.get('self_video')
        self.suppress: bool = data.get('suppress')
        if data.get('request_to_speak_timestamp') is not None:
            self.request_to_speak_timestamp: datetime = convert_iso_timestamp(data.get('request_to_speak_timestamp'))
