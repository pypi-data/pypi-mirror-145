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
from enum import IntEnum
from typing import Optional, Union

# from pydisco.channel import Channel
from pydisco.emoji import Emoji
from pydisco.member import Member
from pydisco.sticker import Sticker
from pydisco.user import User
from pydisco.utils import Snowflake, convert_iso_timestamp


class MessageType(IntEnum):
    """
        This class represents messages' types in Discord.
    """

    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    GUILD_MEMBER_JOIN = 7
    USER_PREMIUM_GUILD_SUBSCRIPTION = 8
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1 = 9
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2 = 10
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3 = 11
    CHANNEL_FOLLOW_ADD = 12
    GUILD_DISCOVERY_DISQUALIFIED = 14
    GUILD_DISCOVERY_REQUALIFIED = 15
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    THREAD_CREATED = 18
    REPLY = 19
    CHAT_INPUT_COMMAND = 20
    THREAD_STARTER_MESSAGE = 21
    GUILD_INVITE_REMINDER = 22
    CONTEXT_MENU_COMMAND = 23


class MessageFlags(IntEnum):
    """
        This class represents message flags in Discord.
    """

    DEFAULT = 0
    CROSS_POSTED = 1 << 0
    IS_CROSS_POST = 1 << 1
    SUPPRESS_EMBEDS = 1 << 2
    SOURCE_MESSAGE_DELETED = 1 << 3
    URGENT = 1 << 4
    HAS_THREAD = 1 << 5
    EPHEMERAL = 1 << 6
    LOADING = 1 << 7
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8


class MessageReference:
    """
        This class represents message reference.
    """

    def __init__(self, data):
        if data.get('message_id') is not None:
            self.message_id: Optional[int] = int(data.get('message_id'))
        if data.get('channel_id') is not None:
            self.channel_id: Optional[int] = int(data.get('channel_id'))
        if data.get('guild_id') is not None:
            self.guild_id: Optional[int] = int(data.get('guild_id'))
        self.fail_if_not_exists: Optional[bool] = data.get('fail_if_not_exists')


class Reaction:
    """
        This class represents reactions.
    """

    def __init__(self, data, http):
        self.count: int = data.get('count')
        self.me: bool = data.get('me')
        self.emoji: Emoji = Emoji(data.get('emoji'), http)


class Message(Snowflake):
    """
        This class represents all messages, that being sent in Discord.
    """

    def __init__(self, data, http, cache):
        self.id: int = int(data.get('id'))
        super().__init__(self.id)
        self.channel_id: int = int(data.get('channel_id'))
        if data.get('guild_id') is not None:
            self.guild_id: Optional[int] = int(data.get('guild_id'))
        self.author: User = User(data.get('author'), http)
        if data.get('member') is not None:
            self.member: Optional[Member] = Member(data.get('member'), http)
        self.content: str = data.get('content')
        self.timestamp: datetime = convert_iso_timestamp(data.get('timestamp'))
        if data.get('edited_timestamp') is not None:
            self.edited_timestamp: Optional[datetime] = convert_iso_timestamp(
                data.get('edited_timestamp'))
        self.tts: bool = data.get('tts')
        self.mention_everyone: bool = data.get('mention_everyone')
        if data.get('mentions') is not None:
            self.mentions: list[User] = list(map(User, data.get('mentions')))
        self.mention_roles: list[int] = list(map(int, data.get('mention_roles')))
        # TODO: attachments, embeds
        if data.get('reactions') is not None:
            self.reactions: Optional[list[Reaction]] = list(map(Reaction, data.get('reactions')))
        self.nonce: Optional[Union[str, int]] = data.get('nonce')
        self.pinned: bool = data.get('pinned')
        if data.get('webhook_id') is not None:
            self.webhook_id: Optional[int] = int(data.get('webhook_id'))
        self.type: MessageType = MessageType(data.get('type'))
        # TODO: activity, application
        if data.get('application_id') is not None:
            self.application_id: Optional[int] = int(data.get('application_id'))
        if data.get('message_reference') is not None:
            self.message_reference: Optional[MessageReference] = MessageReference(
                data.get('message_reference'))
        self.flags: Optional[MessageFlags] = MessageFlags(
            data.get('flags'))
        if data.get('referenced_message') is not None:
            self.referenced_message: Optional[Message] = Message(
                data.get('referenced_message'), http, cache)
        # TODO: interaction
        # if data.get('thread') is not None:
        #     self.thread: Optional[Channel] = Channel(data.get('thread'), http, cache)
        # FIXME
        # TODO: components, sticker_items
        if data.get('stickers') is not None:
            self.stickers: Optional[list[Sticker]] = list(map(Sticker, data.get('stickers')))

        self.__cache = cache

    def __repr__(self) -> str:
        return f'({self.id}) {self.author.username}: {self.content}'

    async def get_channel(self):
        """:class:`Channel` Get the channel to which this message was sent."""
        return await self.__cache.get_channel(self.channel_id)
