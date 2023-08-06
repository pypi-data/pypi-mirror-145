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
from typing import Any, Optional, Union

from pydisco.http import Http
from pydisco.utils import Snowflake


class UserFlags(IntEnum):
    """
        This enum represents flags that can be added to a user's account.
    """
    NONE = 0
    """None"""

    DISCORD_EMPLOYEE = 1 << 0
    """Discord Employee."""

    PARTNERED_SERVER_OWNER = 1 << 1
    """Owner of a partnered Discord server."""

    HYPESQUAD_EVENTS = 1 << 2
    """HypeSquad Events."""

    BUG_HUNTER_LEVEL_1 = 1 << 3
    """Bug Hunter Level 1."""

    HYPESQUAD_BRAVERY = 1 << 6
    """HypeSquad House of Bravery."""

    HYPESQUAD_BRILLIANCE = 1 << 7
    """HypeSquad House of Brilliance."""

    HYPESQUAD_BALANCE = 1 << 8
    """HypeSquad House of Balance."""

    EARLY_SUPPORTER = 1 << 9
    """Early Supporter."""

    TEAM_USER = 1 << 10
    """Team user."""

    BUG_HUNTER_LEVEL_2 = 1 << 14
    """Bug Hunter Level 2."""

    VERIFIED_BOT = 1 << 16
    """Verified Bot."""

    EARLY_VERIFIED_DEVELOPER = 1 << 17
    """Early verified Bot Developer."""

    DISCORD_CERTIFIED_MODERATOR = 1 << 18
    """Discord Certified Moderator."""


class PremiumType(IntEnum):
    """
        This enum represents the types of paid user subscriptions.
    """
    NONE = 0
    """No premium for this user."""

    NITRO_CLASSIC = 1
    """This user have Nitro Classic subscription."""

    FULL_NITRO = 2
    """This user have default Nitro subscription."""


class User(Snowflake):
    """
        This class represents users in Discord.

        Attributes
        ----------
        id : int
            Unique Snowflake ID for this user.
        username : str
            Displayed user's name.
        discriminator : str
            Not a unique set of 4 numbers that are required to find the user's account.
        avatar : str, any
            The hash string of the user's avatar.
        bot : bool, optional
            Is the user a bot?
        system : bool, optional
            Is the user a system?
        mfa_enabled : bool, optional
            Whether two-factor authentication is enabled?
        banner : str, any, optional
             This user's banner hash.
        accent_color : int, any, optional
            Hexadecimal value for color of this user.
        locale : str, optional
            Localization of the user's client.
        verified : bool, optional
            Is the user verified?
        email : str, any, optional
            E-mail address for this user.
        flags : :class:`UserFlags`, optional
            Flags this user.
        premium_type : :class:`PremiumType`, optional
            Type of premium user subscription.
        public_flags : :class:`UserFlags`, optional
            Public flags of the user.

        Methods
        -------
        human : bool
            Is the user a human?
        mention : str
            Mention for this user.
        created_at : datetime
            When this user was created.
    """

    def __init__(self, data, _http: Http) -> None:
        self.id: int = int(data.get('id'))
        super().__init__(self.id)
        self.username: str = data.get('username')
        self.discriminator: int = int(data.get('discriminator'))
        self.avatar: Union[str, Any] = data.get('avatar')
        self.bot: Optional[bool] = data.get('bot')
        self.system: Optional[bool] = data.get('system')
        self.mfa_enabled: Optional[bool] = data.get('mfa_enabled')
        self.banner: Optional[Union[str, Any]] = data.get('banner')
        self.accent_color: Optional[Union[int, Any]] = data.get('accent_color')
        self.locale: Optional[str] = data.get('locale')
        self.verified: Optional[bool] = data.get('verified')
        self.email: Optional[Union[str, Any]] = data.get('email')
        if data.get('flags') is not None:
            self.flags: Optional[UserFlags] = UserFlags(data.get('flags'))
        if data.get('premium_type') is not None:
            self.premium_type: Optional[PremiumType] = PremiumType(data.get('premium_type'))
        # if data.get('public_flags') is not None:
        #    self.public_flags: Optional[UserFlags] = UserFlags(data.get('public_flags'))
        # FIXME 04.04.2022: ValueError: 589824 is not a valid UserFlags

    def __repr__(self) -> str:
        return f'{self.username}#{self.discriminator}'

    @property
    def mention(self) -> str:
        """:str: Mention for this user."""
        return f'<@{self.id}>'

    @property
    def human(self) -> bool:
        """:bool: Is the user a real person?"""
        return not (self.bot and self.system)
