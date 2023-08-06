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
from pydisco.channel import Channel
from pydisco.guild import Guild
from pydisco.user import User


class Cache:
    """
        This class represents caching.

        Attributes
        ----------
        guilds : dict[:class:`Guild`]
            All cached guilds.
        users : dict[:class:`User`]
            All cached users.

        Methods
        -------
        get_guild(guild_id, force=False)
            A method that allows you to get a guild by ID.
        get_user(user_id, force=False)
            A method that allows you to get a user by ID.
    """

    def __init__(self, http) -> None:
        self.guilds: dict[Guild] = {}
        self.users: dict[User] = {}
        self.channels: dict[Channel] = {}
        self.__http = http

    async def get_guild(self, guild_id: int, force: bool = False) -> Guild:
        """Get Guild's instance from cache or fetch it directly from Discord API.

        Parameters
        ----------
        guild_id : int
            Id of the guild to fetch.
        force : bool
            Use force-fetch? Defaults to `False`.

        Returns
        -------
        :class:`Guild`
            Fetched Guild's instance.
        """
        fetched = self.guilds.get(guild_id)  # type: ignore
        if not self.guilds.__contains__(guild_id) or force or fetched.unavailable:
            fetched = await self.__http.get_guild(guild_id)
        if not self.guilds.__contains__(guild_id):
            self.guilds[guild_id] = fetched  # type: ignore
        return Guild(fetched, self, self.__http)

    async def get_user(self, user_id: int, force: bool = False) -> User:
        """Get User's instance from cache or fetch it directly from Discord API.

        Parameters
        ----------
        user_id : int
            Id of the user to fetch.
        force : bool
            Use force-fetch? Defaults to `False`.

        Returns
        -------
        :class:`User`
            Fetched User's instance.
        """
        fetched = self.users.get(user_id)  # type: ignore
        if not self.users.__contains__(user_id) or force:
            fetched = await self.__http.get_user(user_id)
        if not self.users.__contains__(user_id):
            self.users[user_id] = fetched  # type: ignore
        return User(fetched, self.__http)

    async def get_channel(self, channel_id: int, force: bool = False) -> Channel:
        """Get channel's instance from cache or fetch it directly from Discord API.

        Parameters
        ----------
        channel_id : int
            Id of the channel to fetch.
        force : bool
            Use force-fetch? Defaults to `False`.

        Returns
        -------
        :class:`Channel`
            Fetched Channel's instance.
        """
        fetched = self.channels.get(channel_id)  # type: ignore
        if not self.channels.__contains__(channel_id) or force:
            fetched = await self.__http.get_channel(channel_id)
        if not self.channels.__contains__(channel_id):
            self.channels[channel_id] = fetched  # type: ignore
        return Channel(fetched, self.__http, self)
