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

import logging
from asyncio import get_event_loop, sleep, new_event_loop, AbstractEventLoop
from json import loads
from platform import platform
from threading import Thread
from typing import Coroutine, Any, Optional

from aiohttp import ClientWebSocketResponse
from aiohttp.web_ws import WebSocketResponse

from pydisco.cache import Cache
from pydisco.guild import Guild
from pydisco.http import Http
from pydisco.intents import Intents
from pydisco.message import Message
from pydisco.user import User

_logger = logging.getLogger('pydisco')


async def heartbeat_send(
        ws: WebSocketResponse, last_sequence: Optional[int], heartbeat_interval: int
) -> None:
    """The simplest method for sending a heartbeat request to the Discord WebSocket API.

    Parameters
    ----------
    ws : WebSocketResponse
        WebSocket for sending data.
    last_sequence : :class:`Optional[int]`
        Last sequence number received.
    heartbeat_interval : int
        How often to send a request to the Discord server.
    """
    while True:
        await sleep(heartbeat_interval)
        await ws.send_json({'op': 1, 'd': last_sequence})
        _logger.debug('Heartbeat sent!')


def heartbeat_wrapper(
        ws: WebSocketResponse, last_sequence: Optional[int], heartbeat_interval: int
) -> None:
    """A wrapper for the heartbeat function method.

    Parameters
    ----------
    ws : WebSocketResponse
        WebSocket for sending data.
    last_sequence : :class:`Optional[int]`
        Last sequence number received.
    heartbeat_interval : int
        How often to send a request to the Discord server.
    """
    new_event_loop().run_until_complete(heartbeat_send(ws, last_sequence, heartbeat_interval))


class Client:
    """
        Main pydisco class for working with Discord API.
        All starts from here.

        Attributes
        ----------
        ready : bool
            Shows if the bot is ready to work.
        user : User
            Bot user.
        intents : int
            Applied Gateway intents.
        cache : Cache
            Caching module.

        Methods
        -------
        on(event_name)
            Decorator function for listening to client's events.
        run(token)
            A method for starting a bot.
        stop()
            A method to stop the bot if it's running.
    """

    def __init__(self, token: str, **kwargs) -> None:
        # Event loop of the current process for asynchronous tasks.
        self.__event_loop: AbstractEventLoop = get_event_loop()

        # Listeners of the client's events.
        self.__listeners: dict = {}

        # Indicates, if client is ready.
        self.ready: bool = False

        # User of client, if it's ready.
        self.user = None

        # Intents for this bot.
        self.intents: int = kwargs.get('intents', Intents.ALL)

        # Custom gateway version from user.
        self.__gv: int = kwargs.get('gateway_version', 9)

        # WebSocket instance for this client's session.
        self.__ws: Optional[ClientWebSocketResponse] = None

        # Token for client in string.
        self.__token: str = token

        # Own http module for working with WebSockets and HTTP.
        self.__http: Http = Http(token, self.__gv)

        # Caching for our client.
        self.cache: Cache = Cache(self.__http)

    def on(self, event_name: str):
        """Decorator function for listening to client's events.

        Parameters
        ----------
        event_name : str
            The name of the event for listening.

        Examples
        --------
        @client.on('ready')
        async def on_ready():
            print('Client is now ready!')

        Returns
        -------
        :class:`function`
            A function that has been specified as a decorator function.
        """

        def handle(function: Coroutine) -> Coroutine:
            """Handler function for event processing.

            Parameters
            ----------
            function : Coroutine
                The function that will be called when the event is fired up.

            Returns
            -------
            :class:`Coroutine`
                Specified function.
            """
            # There are can be no registered event, so create array for it.
            if event_name not in self.__listeners:
                self.__listeners[event_name] = []
            # Appending specified Coroutine function to the specified event.
            self.__listeners[event_name].append(function)
            return function

        return handle

    async def __emit(self, event_name: str, *args, **kwargs) -> None:
        """The main function for fire up events.

        Parameters
        ----------
        event_name : str
            The name of the event for listening.
        """
        # If there are will be no listeners for current event, Python will throw KeyError.
        # So, checking it to avoid errors.
        if event_name in self.__listeners:
            for listener in self.__listeners[event_name]:
                await listener(*args, **kwargs)

    def run(self) -> None:
        """A method for starting a bot."""
        self.__event_loop.run_until_complete(self.__login())

    async def __login(self) -> None:
        # Warning: there are a lot of undocumented code... heh
        _logger.debug('Connecting to the Gateway. Using %d version and `json` encoding.'
                      % self.__gv)
        self.__ws = await self.__http.create_websocket()
        msg = await self.__ws.receive_json()
        _logger.debug('Received the first response from the Gateway: %s' % msg)
        thread = Thread(target=heartbeat_wrapper,
                        args=(self.__ws, msg['s'], int(msg['d']['heartbeat_interval']) / 1000))
        thread.start()

        await self.__ws.send_json({
            'op': 2,
            'd': {
                'token': self.__token,
                'intents': self.intents,
                'properties': {
                    '$os': platform(),
                    '$browser': 'pydisco',
                    '$device': 'pydisco'
                }
            }
        })
        _logger.debug('A opcode for bot registration (2) has been sent.')

        gateway_data = await self.__http.get_gateway()
        session_start_limit = gateway_data.get('session_start_limit')
        total = session_start_limit.get('total')
        remaining = session_start_limit.get('remaining')
        reset_in = session_start_limit.get('reset_after')
        _logger.debug('Received `session_start_limit` information. This client has %d/%d '
                      'reconnections available. Reset will be in %d.'
                      % (remaining, total, reset_in))

        async for message in self.__ws:
            raw = loads(message.data)
            await self.__emit('event', raw)

            event_name: str = raw['t']
            data: Any = raw['d']

            _logger.debug('The bot received a `%s` event from the Gateway.' % event_name)
            _logger.debug('Received new message from Gateway: %s.' % raw)

            if event_name == 'READY':
                self.user = User(data['user'], self.__http)
                self.ready = True
                await self.__emit('ready')
                _logger.debug('Bot is now ready. Session id: %s.', data['session_id'])
            elif event_name == 'GUILD_CREATE':
                guild = Guild(data, self.__http, self.cache)
                self.cache.guilds[guild.id] = guild  # type: ignore
                await self.__emit('guild_create', guild)
            elif event_name == 'MESSAGE_CREATE':
                created_message = Message(data, self.__http, self.cache)
                await self.__emit('message_create', created_message)
            elif event_name is None:
                pass
            else:
                _logger.debug('[ERROR] Received unhandled event from Discord.')

    def stop(self) -> None:
        """A method to stop the bot if it's running."""
        self.__event_loop.run_until_complete(self.__stop())

    async def __stop(self) -> None:
        if self.__http.is_session_closed:
            return
        await self.__http.close_session()
        await self.__ws.close()
