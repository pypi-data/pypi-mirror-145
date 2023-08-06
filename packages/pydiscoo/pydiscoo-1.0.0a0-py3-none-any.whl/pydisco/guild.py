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
from typing import Union, Any, Optional

from pydisco.channel import Channel
from pydisco.emoji import Emoji
from pydisco.member import Member
from pydisco.voice import VoiceState
from pydisco.presence import Presence
from pydisco.role import Role
from pydisco.sticker import Sticker
from pydisco.utils import Snowflake, convert_iso_timestamp


class VerificationLevel(IntEnum):
    """
        This enum represents verification level in Discord.
    """

    NONE = 0
    """Unrestricted."""

    LOW = 1
    """Must have verified email on account."""

    MEDIUM = 2
    """Must be registered on Discord for longer than 5 minutes."""

    HIGH = 3
    """Must be a member of the server for longer than 10 minutes."""

    VERY_HIGH = 4
    """Must have a verified phone number."""


class NotificationsLevel(IntEnum):
    """
        This enum represents notifications level in Discord.
    """

    ALL_MESSAGES = 0
    """Members will receive notifications for all messages by default."""

    ONLY_MENTIONS = 1
    """Members will receive notifications only for messages that @mention them by default."""


class ExplicitContentLevel(IntEnum):
    """
        This enum represents explicit content level in Discord.
    """

    DISABLED = 0
    """Media content will not be scanned."""

    MEMBERS_WITHOUT_ROLES = 1
    """Media content sent by members without roles will be scanned."""

    ALL_MEMBERS = 2
    """Media content sent by all members will be scanned."""


class MFALevel(IntEnum):
    """
        This enum represents MFA level in Discord.
    """

    NONE = 0
    """Guild has no MFA/2FA requirement for moderation actions."""

    ELEVATED = 1
    """Guild has a 2FA requirement for moderation actions."""


class PremiumTier(IntEnum):
    """
        This enum represents premium tier in Discord.
    """

    NONE = 0
    """Guild has not unlocked any Server Boost perks."""

    TIER_1 = 1
    """Guild has unlocked Server Boost level 1 perks."""

    TIER_2 = 2
    """Guild has unlocked Server Boost level 2 perks."""

    TIER_3 = 3
    """Guild has unlocked Server Boost level 3 perks."""


class NSFWLevel(IntEnum):
    """
        This class represents NSFW level in Discord.
    """

    DEFAULT = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3


class WelcomeScreen:
    """
        This class represents welcome screen in Discord.

        Attributes
        ----------
        description : str
            The server description shown in the welcome screen.
        welcome_channels : list[WelcomeScreenChannel]
            The channels shown in the welcome screen, up to 5.
    """

    def __init__(self, data):
        self.description: str = data.get('description')
        self.welcome_channels: list[WelcomeScreenChannel] = list(
            map(WelcomeScreenChannel, data.get('welcome_channels')))


class WelcomeScreenChannel:
    """
        This class represents welcome screen channel in Discord.

        Attributes
        ----------
        channel_id : int
            The channel's id.
        description : str
            The description shown for the channel.
        emoji_id : Union[int, Any]
            The emoji id, if the emoji is custom.
        emoji_name : Union[str, Any]
            The emoji name if custom, the unicode character if standard, or None if no emoji is set.
    """

    def __init__(self, data):
        self.channel_id: int = data.get('channel_id')
        self.description: str = data.get('description')
        self.emoji_id: Union[int, Any] = data.get('emoji_id')
        self.emoji_name: Union[str, None] = data.get('emoji_name')


class Guild(Snowflake):
    """
        This enum represents Guilds in Discord.
    """

    def __init__(self, data, http, cache):
        self.id: int = data.get('id')
        super().__init__(self.id)
        self.name: str = data.get('name')
        self.icon: Union[str, Any] = data.get('icon')
        self.icon_hash: Optional[Union[str, Any]] = data.get('icon_hash')
        self.splash: Union[str, Any] = data.get('splash')
        self.discovery_splash: Union[str, Any] = data.get('discovery_splash')
        self.owner: Optional[bool] = data.get('owner')
        self.owner_id: int = data.get('owner_id')
        self.permissions: Optional[str] = data.get('permissions')
        self.afk_channel_id: Union[int, None] = data.get('afk_channel_id')
        self.afk_timeout: int = data.get('afk_timeout')
        self.widget_enabled: Optional[bool] = data.get('widget_enabled')
        self.widget_channel_id: Optional[Union[int, Any]] = data.get('widget_channel_id')
        self.verification_level: VerificationLevel = VerificationLevel(data.get('verification_level'))
        self.default_message_notifications: NotificationsLevel = NotificationsLevel(
            data.get('default_message_notifications'))
        self.explicit_content_filter: ExplicitContentLevel = ExplicitContentLevel(data.get('explicit_content_filter'))
        self.roles: list[Role] = list(map(Role, data.get('roles')))
        self.emojis: list[Emoji] = [Emoji(emoji, http) for emoji in data.get('emojis')]
        self.features: list[str] = data.get('features')
        self.mfa_level: MFALevel = MFALevel(data.get('mfa_level'))
        self.application_id: Union[int, Any] = data.get('application_id')
        self.system_channel_id: Union[int, Any] = data.get('system_channel_id')
        self.rules_channel_id: Union[int, Any] = data.get('rules_channel_id')
        if data.get('joined_at') is not None:
            self.joined_at: Optional[datetime] = convert_iso_timestamp(data.get('joined_at'))
        self.large: Optional[bool] = data.get('large')
        self.unavailable: Optional[bool] = data.get('unavailable')
        self.member_count: Optional[int] = data.get('member_count')
        if data.get('voice_states') is not None:
            self.voice_states: Optional[list[VoiceState]] = [VoiceState(state, http) for state in
                                                             data.get('voice_states')]
        if data.get('members') is not None:
            self.members: Optional[list[Member]] = [Member(member, http) for member in data.get('members')]
        if data.get('channels') is not None:
            self.channels: Optional[list[Channel]] = [Channel(channel, http, cache) for channel in data.get('channels')]
        if data.get('threads') is not None:
            self.threads: Optional[list[Channel]] = [Channel(channel, http, cache) for channel in data.get('threads')]
        if data.get('presences') is not None:
            self.presences: Optional[list[Presence]] = [Presence(presence, http) for presence in data.get('presences')]
        self.max_presences: Optional[Union[int, Any]] = data.get('max_presences')
        self.max_members: Optional[int] = data.get('max_members')
        self.vanity_url_code: Union[str, Any] = data.get('vanity_url_code')
        self.description: Union[str, Any] = data.get('description')
        self.banner: Union[str, Any] = data.get('banner')
        self.premium_tier: PremiumTier = PremiumTier(data.get('premium_tier'))
        self.premium_subscription_count: Optional[int] = data.get('premium_subscription_count')
        self.preferred_locale: str = data.get('preferred_locale')
        self.public_updates_channel_id: Union[int, Any] = data.get('public_updates_channel_id')
        self.max_video_channel_users: Optional[int] = data.get('max_video_channel_users')
        self.approximate_member_count: Optional[int] = data.get('approximate_member_count')
        self.approximate_presence_count: Optional[int] = data.get('approximate_presence_count')
        if data.get('welcome_screen') is not None:
            self.welcome_screen: Optional[WelcomeScreen] = WelcomeScreen(data.get('welcome_screen'))
        self.nsfw_level: NSFWLevel = NSFWLevel(data.get('nsfw_level'))
        # TODO: stage_instances
        if data.get('stickers') is not None:
            self.stickers: Optional[list[Sticker]] = [Sticker(sticker, http) for sticker in data.get('stickers')]
        # TODO: guild_scheduled_events
        self.premium_progress_bar_enabled: bool = data.get('premium_progress_bar_enabled')
