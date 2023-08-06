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
from typing import Optional, Union, Any

from pydisco.emoji import Emoji
from pydisco.utils import convert_timestamp


class ActivityType(IntEnum):
    """
        This enum represents activity types in Discord.
    """

    GAME = 0
    """
        Format: Playing {name}
        Example: "Playing Rocket League"
    """

    STREAMING = 1
    """
        Format: Streaming {details}
        Example: "Streaming Rocket League"
    """

    LISTENING = 2
    """
        Format: Listening to {name}
        Example: "Listening to Spotify"
    """

    WATCHING = 3
    """
        Format: Watching {name}
        Example: "Watching YouTube Together"
    """

    CUSTOM = 4
    """
        Format: {emoji} {name}
        Example: ":smiley: I am cool"
    """

    COMPETING = 5
    """
        Format: Competing in {name}
        Example: "Competing in Arena World Champions"
    """


class ActivityFlags(IntEnum):
    """
        This enum represents activity flags in Discord.
    """

    INSTANCE = 1 << 0
    JOIN = 1 << 1
    SPECTATE = 1 << 2
    JOIN_REQUEST = 1 << 3
    SYNC = 1 << 4
    PLAY = 1 << 5
    PARTY_PRIVACY_FRIENDS = 1 << 6
    PARTY_PRIVACY_VOICE_CHANNEL = 1 << 7
    EMBEDDED = 1 << 8


class Party:
    """
        This class represents activity parties in Discord.

        Attributes
        ----------
        id : Optional[str]
            The id of the party.
        size : Optional[list[int]]
            Used to show the party's current and maximum size.
    """

    def __init__(self, data):
        self.id: Optional[str] = data.get('id')
        self.size: Optional[list[int]] = data.get('size')


class Assets:
    """
        This class represents activity assets in Discord.

        Attributes
        ----------
        large_image : Optional[str]
            Activity Asset Image.
        large_text : Optional[str]
            Text displayed when hovering over the large image of the activity.
        small_image : Optional[str]
            Activity Asset Image.
        small_text : Optional[str]
            Text displayed when hovering over the small image of the activity.
    """

    def __init__(self, data):
        self.large_image: Optional[str] = data.get('large_image')
        self.large_text: Optional[str] = data.get('large_text')
        self.small_image: Optional[str] = data.get('small_image')
        self.small_text: Optional[str] = data.get('small_text')


class Button:
    """
        This class represents activity buttons in Discord.

        Attributes
        ----------
        label : str
            The text shown on the button (1-32 characters).
        url : str
            The url opened when clicking the button (1-512 characters).
    """

    def __init__(self, data):
        self.label: str = data.get('label')
        self.url: str = data.get('url')


class Secrets:
    """
        This class represents activity secrets in Discord.

        Attributes
        ----------
        join : Optional[str]
            The secret for joining a party.
        spectate : Optional[str]
            The secret for spectating a game.
        match : Optional[str]
            The secret for a specific instanced match.
    """

    def __init__(self, data):
        self.join: Optional[str] = data.get('join')
        self.spectate: Optional[str] = data.get('spectate')
        self.match: Optional[str] = data.get('match')


class Activity:
    """
        This class represents activities in Discord.

        Attributes
        ----------
        name : str
            The activity's name.
        type : ActivityType
            Activity type.
        url : Optional[Union[str, Any]]
            Stream url, is validated when type is 1.
        created_at : datetime
            Datetime instance that represents when the activity was added to the user's session.
        application_id : Optional[int]
            Application id for the game.
        details : Optional[Union[str, Any]]
            What the player is currently doing.
        state : Optional[Union[str, Any]]
            The user's current party status.
        emoji : Optional[Emoji]
            The emoji used for a custom status.
        party : Optional[Party]
            Information for the current party of the player.
        assets : Optional[Assets]
            Images for the presence and their hover texts.
        secrets : Optional[Secrets]
            Secrets for Rich Presence joining and spectating.
        instance : Optional[bool]
            Whether or not the activity is an instanced game session.
        flags : Optional[ActivityFlags]
            Describes what the payload includes.
        buttons : Optional[list[Button]]
            The custom buttons shown in the Rich Presence (max 2).
    """

    def __init__(self, data, http):
        self.name: str = data.get('name')
        self.type: ActivityType = ActivityType(data.get('type'))
        self.url: Optional[Union[str, Any]] = data.get('url')
        self.created_at: datetime = convert_timestamp(int(int(data.get('created_at')) / 1000))
        if data.get('application_id') is not None:
            self.application_id: Optional[int] = int(data.get('application_id'))
        self.details: Optional[Union[str, Any]] = data.get('details')
        self.state: Optional[Union[str, Any]] = data.get('state')
        if data.get('emoji') is not None:
            self.emoji: Optional[Emoji] = Emoji(data.get('emoji'), http)
        if data.get('party') is not None:
            self.party: Optional[Party] = Party(data.get('party'))
        if data.get('assets') is not None:
            self.assets: Optional[Assets] = Assets(data.get('assets'))
        if data.get('secrets') is not None:
            self.secrets: Optional[Secrets] = Secrets(data.get('secrets'))
        self.instance: Optional[bool] = data.get('instance')
        if data.get('flags') is not None:
            self.flags: Optional[ActivityFlags] = ActivityFlags(data.get('flags'))
        if data.get('buttons') is not None:
            self.buttons: Optional[list[Button]] = list(map(Button, data.get('buttons')))
