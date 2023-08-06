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

from aiohttp import ClientSession, ClientWebSocketResponse

from . import __version__


class Http:
    """
        This class contains main methods for interacting with HTTP and WebSocket API.
    """

    def __init__(self, token: str, version: int = 9) -> None:
        self.__session: ClientSession = ClientSession()
        self.__version = version
        self.__headers = {
            'User-Agent': f'DiscordBot (https://github.com/Pelfox/pydisco, {__version__})',
            'Authorization': f'Bot {token}', 'Content-Type': 'application/json'
        }
        self.base_url = f'https://discord.com/api/v{self.__version}/'

    async def get_user(self, user_id: int) -> dict:
        """:dict: Method for getting user."""
        return await self.__perform_request('GET', f'users/{user_id}')

    async def get_guild(self, guild_id: int) -> dict:
        """:dict: Get Guild via ID."""
        return await self.__perform_request('GET', f'guilds/{guild_id}')

    async def get_channel(self, channel_id: int) -> dict:
        """:dict: Get Channel via ID."""
        return await self.__perform_request('GET', f'/channels/{channel_id}')

    async def get_gateway(self) -> dict:
        """:dict: Method for getting statistic and other information about gateway."""
        return await self.__perform_request('GET', 'gateway/bot')

    async def create_websocket(self) -> ClientWebSocketResponse:
        """Method for creating new WebSocket connection."""
        return await self.__session.ws_connect(f'wss://gateway.discord.gg/'
                                               f'?v={self.__version}&encoding=json')

    async def post_message(self, channel_id: int, content: str, tts: bool) -> dict:
        """:dict: Post a new message to specific channel."""
        return await self.__perform_request('POST', f'/channels/{channel_id}/messages',
                                            json={'content': content, 'tts': tts})

    async def __perform_request(self, method: str, endpoint: str, **kwargs) -> Optional[dict]:
        async with self.__session.request(
                method, f'{self.base_url}{endpoint}', headers=self.__headers, **kwargs
        ) as response:
            # idk why aiohttp throws an error to me without it... so, I'll simply
            # put this peace of code here... also idk why I'm writing this comment
            # TODO: checks
            response_data = await response.json(encoding='UTF-8')
            response.close()

            if 'retry_after' in response_data:
                print('error: rate limited')
                return  # TODO: throw error

            if not kwargs.get('disable_return'):
                return response_data
            return None

    @property
    def is_session_closed(self) -> bool:
        """:bool: Is session now closed?"""
        return self.__session.closed

    async def close_session(self) -> None:
        """:None: Closes current session."""
        await self.__session.close()
