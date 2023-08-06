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

from enum import IntEnum
from typing import Optional, Any, Union

from pydisco.message import Message
from pydisco.utils import Snowflake


class ChannelType(IntEnum):
    """
        This class represents Discord's enum of channel types.
    """
    GUILD_TEXT = 0
    """This channel belongs to text channel in guild."""

    DM = 1
    """This channel belongs to direct message channel."""

    GUILD_VOICE = 2
    """This channel belongs to voice channel in guild."""

    GROUP_DM = 3
    """This channel belongs to group direct message."""

    GUILD_CATEGORY = 4
    """This channel is guild's category."""

    GUILD_NEWS = 5
    """This channel belongs to guild's news."""

    GUILD_STORE = 6
    """This channel belongs to guild's store."""

    GUILD_NEWS_THREAD = 10
    """This channel belongs to guild's news thread."""

    GUILD_PUBLIC_THREAD = 11
    """This channel belongs to guild's public thread."""

    GUILD_PRIVATE_THREAD = 12
    """This channel belongs to guild's private thread."""

    GUILD_STAGE_VOICE = 13
    """This channel belongs to guild's stage voice."""


class VideoQualityMode(IntEnum):
    """
        This class represents video quality mode in voice channels.
    """
    AUTO = 1
    """Discord will automatically choose the quality for optimal performance."""

    FULL = 2
    """720p"""


class Channel(Snowflake):
    """
        This class represents any channel in Discord.

        Attributes
        ----------
        id : int
            Unique Snowflake ID for this channel.
        type : :class:`ChannelType`
            Type of this channel, represented in enum.
    """

    def __init__(self, data, http, cache):
        self.id: int = int(data.get('id'))
        super().__init__(self.id)
        self.type: ChannelType = ChannelType(data.get('type'))
        if data.get('guild_id') is not None:
            self.guild_id: Optional[int] = int(data.get('guild_id'))
        if data.get('position') is not None:
            self.position: Optional[int] = int(data.get('position'))
        # TODO: permission_overwrites
        self.name: Optional[str] = data.get('name')
        # TODO: recipients
        if data.get('owner_id') is not None:
            self.owner_id: Optional[int] = int(data.get('owner_id'))
        if data.get('application_id') is not None:
            self.application_id: Optional[int] = int(data.get('application_id'))
        self.parent_id: Optional[Union[int, Any]] = data.get('parent_id')
        # TODO: last_pin_timestamp, rtc_region
        # TODO: thread_metadata, member
        self.permissions = data.get('permissions')
        self.topic: Optional[Union[str, Any]] = data.get('topic')
        self.nsfw: Optional[bool] = data.get('nsfw')
        self.last_message_id: Optional[Union[int, Any]] = data.get('last_message_id')
        self.default_auto_archive_duration = data.get('default_auto_archive_duration')
        self.icon: Optional[Union[str, Any]] = data.get('icon')
        if data.get('rate_limit_per_user') is not None:
            self.rate_limit_per_user: Optional[int] = int(data.get('rate_limit_per_user'))
        if data.get('message_count') is not None:
            self.message_count: Optional[int] = int(data.get('message_count'))
        if data.get('member_count') is not None:
            self.member_count: Optional[int] = int(data.get('member_count'))
        if data.get('bitrate') is not None:
            self.bitrate: Optional[int] = int(data.get('bitrate'))
        if data.get('user_limit') is not None:
            self.user_limit: Optional[int] = int(data.get('user_limit'))
        if data.get('video_quality_mode') is not None:
            self.video_quality_mode: Optional[int] = VideoQualityMode(
                data.get('video_quality_mode'))

        self.__cache = cache
        self.__http = http

    def __repr__(self) -> str:
        return f'Channel[id={self.id}, type={self.type}]'

    async def send_message(self, content: str, tts: bool = False) -> Message:
        """:class:`Message` Method for sending messages into this channel."""
        if ChannelType.GUILD_VOICE in (self.type,) or ChannelType.GUILD_STAGE_VOICE in (self.type,):
            raise Exception("You can't send message into voice channels!")
        data = await self.__http.post_message(self.id, content, tts)
        if data is not None:
            return Message(data, self.__http, self.__cache)
