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
from typing import Optional, Union

from pydisco.user import User
from pydisco.utils import Snowflake


class StickerType(IntEnum):
    """
        This class represents sticker types in Discord.
    """

    STANDARD = 1
    """An official sticker in a pack, part of Nitro or in a removed purchasable pack."""

    GUILD = 2
    """A sticker uploaded to a Boosted guild for the guild's members."""


class StickerFormatType(IntEnum):
    """
        This clas represents sticker format types in Discord.
    """

    PNG = 1
    APNG = 2
    LOTTIE = 3


class Sticker(Snowflake):
    """
        This class represents stickers in Discord.

        Attributes
        ----------
        id : int
            Unique Snowflake ID for this sticker.
        pack_id : int
            For standard stickers, id of the pack the sticker is from.
        name : str
            Name of the sticker.
        description : str
            Description of the sticker.
        tags : str
            Autocomplete/suggestion tags for the sticker (max 200 characters).
        type : :class:`StickerType`
            Type of sticker.
        format_type : :class:`StickerFormatType`
            Type of sticker format.
        available : Optional[bool]
            Whether this guild sticker can be used, may be false due to loss of Server Boosts.
        guild_id : Optional[int]
            Id of the guild that owns this sticker.
        user : Optional[User]
            The user that uploaded the guild sticker.
        sort_value : int
            The standard sticker's sort order within its pack.
    """

    def __init__(self, data, http):
        self.id: int = int(data.get('id'))
        super().__init__(self.id)
        if data.get('pack_id') is not None:
            self.pack_id: Optional[int] = int(data.get('pack_id'))
        self.name: str = data.get('name')
        self.description: Union[str, None] = data.get('description')
        self.tags: str = data.get('tags')
        self.type: StickerType = StickerType(data.get('type'))
        self.format_type: StickerFormatType = StickerFormatType(data.get('format_type'))
        self.available: Optional[bool] = data.get('available')
        self.guild_id: Optional[int] = int(data.get('guild_id'))
        if data.get('user') is not None:
            self.user: Optional[User] = User(data.get('user'), http)
        if data.get('sort_value') is not None:
            self.sort_value: Optional[int] = int(data.get('sort_value'))
