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


class Intents(IntEnum):
    """
        This class represents Gateway intents in Discord.
    """
    NONE = 0
    """No intents will be added to the connection to the Gateway server."""

    GUILDS = 1 << 0
    """
        This intent contains the following events:
        * GUILD_CREATE
        * GUILD_UPDATE
        * GUILD_DELETE
        * GUILD_ROLE_CREATE
        * GUILD_ROLE_UPDATE
        * GUILD_ROLE_DELETE
        * CHANNEL_CREATE
        * CHANNEL_UPDATE
        * CHANNEL_DELETE
        * CHANNEL_PINS_UPDATE
        * THREAD_CREATE
        * THREAD_UPDATE
        * THREAD_DELETE
        * THREAD_LIST_SYNC
        * THREAD_MEMBER_UPDATE
        * THREAD_MEMBERS_UPDATE
        * STAGE_INSTANCE_CREATE
        * STAGE_INSTANCE_UPDATE
        * STAGE_INSTANCE_DELETE
    """

    GUILD_MEMBERS = 1 << 1
    """
        This intent contains the following events:
        * GUILD_MEMBER_ADD
        * GUILD_MEMBER_UPDATE
        * GUILD_MEMBER_REMOVE
        * THREAD_MEMBERS_UPDATE
    """

    GUILD_BANS = 1 << 2
    """
        This intent contains the following events:
        * GUILD_BAN_ADD
        * GUILD_BAN_REMOVE
    """

    GUILD_EMOJIS_AND_STICKERS = 1 << 3
    """
        This intent contains the following events:
        * GUILD_EMOJIS_UPDATE
        * GUILD_STICKERS_UPDATE
    """

    GUILD_INTEGRATIONS = 1 << 4
    """
        This intent contains the following events:
        * GUILD_INTEGRATIONS_UPDATE
        * INTEGRATION_CREATE
        * INTEGRATION_UPDATE
        * INTEGRATION_DELETE
    """

    GUILD_WEBHOOKS = 1 << 5
    """
        This intent contains the following events:
        * WEBHOOKS_UPDATE
    """

    GUILD_INVITES = 1 << 6
    """
        This intent contains the following events:
        * INVITE_CREATE
        * INVITE_DELETE
    """

    GUILD_VOICE_STATES = 1 << 7
    """
        This intent contains the following events:
        * VOICE_STATE_UPDATE
    """

    GUILD_PRESENCES = 1 << 8
    """
        This intent contains the following events:
        * PRESENCE_UPDATE
    """

    GUILD_MESSAGES = 1 << 9
    """
        This intent contains the following events:
        * MESSAGE_CREATE
        * MESSAGE_UPDATE
        * MESSAGE_DELETE
        * MESSAGE_DELETE_BULK
    """

    GUILD_MESSAGE_REACTIONS = 1 << 10
    """
        This intent contains the following events:
        * MESSAGE_REACTION_ADD
        * MESSAGE_REACTION_REMOVE
        * MESSAGE_REACTION_REMOVE_ALL
        * MESSAGE_REACTION_REMOVE_EMOJI
    """

    GUILD_MESSAGE_TYPING = 1 << 11
    """
        This intent contains the following events:
        * TYPING_START
    """

    GUILD_SCHEDULED_EVENTS = 1 << 16
    """
        This intent contains the following events:
        * GUILD_SCHEDULED_EVENT_CREATE
        * GUILD_SCHEDULED_EVENT_UPDATE
        * GUILD_SCHEDULED_EVENT_DELETE
        * GUILD_SCHEDULED_EVENT_USER_ADD
        * GUILD_SCHEDULED_EVENT_USER_REMOVE
    """

    DIRECT_MESSAGES = 1 << 12
    """
        This intent contains the following events:
        * MESSAGE_CREATE
        * MESSAGE_UPDATE
        * MESSAGE_DELETE
        * CHANNEL_PINS_UPDATE
    """

    DIRECT_MESSAGE_REACTIONS = 1 << 13
    """
        This intent contains the following events:
        * MESSAGE_REACTION_ADD
        * MESSAGE_REACTION_REMOVE
        * MESSAGE_REACTION_REMOVE_ALL
        * MESSAGE_REACTION_REMOVE_EMOJI
    """

    DIRECT_MESSAGE_TYPING = 1 << 14
    """
        This intent contains the following events:
        * TYPING_START
    """

    ALL_GUILD = (
            GUILDS | GUILD_BANS | GUILD_MESSAGES | GUILD_MEMBERS |
            GUILD_INVITES | GUILD_INTEGRATIONS | GUILD_EMOJIS_AND_STICKERS |
            GUILD_WEBHOOKS | GUILD_PRESENCES | GUILD_MESSAGE_TYPING |
            GUILD_MESSAGE_REACTIONS | GUILD_VOICE_STATES | GUILD_SCHEDULED_EVENTS
    )
    """All available intents for guilds."""

    ALL_DM = (
            DIRECT_MESSAGES | DIRECT_MESSAGE_REACTIONS |
            DIRECT_MESSAGE_TYPING
    )
    """All available intents for DMs."""

    ALL = ALL_GUILD | ALL_DM
    """In general, all available intents."""

    @staticmethod
    def from_int(intents):
        """:class:`Intents` convert integer into Intents instance."""
        return Intents(intents)
