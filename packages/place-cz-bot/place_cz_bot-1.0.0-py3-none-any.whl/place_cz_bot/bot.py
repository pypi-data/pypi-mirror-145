from __future__ import annotations

import argparse
import asyncio
import json
import logging
import random
import re
import string
import warnings
from datetime import datetime, timedelta
from io import BytesIO
from typing import Optional

import aiohttp
import matplotlib
import matplotlib.pyplot as plt
import numpy
from rich.logging import RichHandler

from .version import __version__

"""
Headless reddit /r/place 2022 updater.

This Python bot is a terminal application that will automatically update
r/place pixels from our command and control server. It supports multiple
reddit accounts and automatically obtains and refreshed access tokens.

Authors:
- /u/tr4ce

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

logger = logging.getLogger()
logging.basicConfig(format=r"[%(name)s] %(message)s", handlers=[RichHandler()])

REDDIT_LOGIN_GET = "https://www.reddit.com/login/?experiment_d2x_2020ify_buttons=enabled&experiment_d2x_sso_login_link=enabled&experiment_d2x_google_sso_gis_parity=enabled&experiment_d2x_onboarding=enabled"
REDDIT_LOGIN_POST = "https://www.reddit.com/login"
REDDIT_PLACE_URL = "https://www.reddit.com/r/place/"
REDDIT_PLACE_SET_PIXEL_URL = "https://gql-realtime-2.reddit.com/query"
PLACE_WEBSOCKET = "wss://gql-realtime-2.reddit.com/query"
CNC_WEBSOCKET = "wss://placecz.martinnemi.me/api/ws"
DEFAULT_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0"

GRAPHQL_CANVAS_QUERY = """
subscription replace($input: SubscribeInput!) {
    subscribe(input: $input) {
        id
        ... on BasicMessage {
            data {
                __typename
                ... on FullFrameMessageData {
                    __typename
                    name
                    timestamp
                }
            }
            __typename
        }
        __typename
    }
}""".strip()

SET_PIXEL_QUERY = """
mutation setPixel($input: ActInput!) {
    act(input: $input) {
        data {
            ... on BasicMessage {
                id
                data {
                    ... on GetUserCooldownResponseMessageData {
                        nextAvailablePixelTimestamp
                        __typename
                    }
                    ... on SetPixelResponseMessageData {
                        timestamp
                        __typename
                    }
                    __typename
                }
                __typename
            }
            __typename
        }
        __typename
    }
}""".strip()

COLOR_MAPPINGS = {
    '#BE0039': 1,
    '#FF4500': 2,
    '#FFA800': 3,
    '#FFD635': 4,
    '#00A368': 6,
    '#00CC78': 7,
    '#7EED56': 8,
    '#00756F': 9,
    '#009EAA': 10,
    '#2450A4': 12,
    '#3690EA': 13,
    '#51E9F4': 14,
    '#493AC1': 15,
    '#6A5CFF': 16,
    '#811E9F': 18,
    '#B44AC0': 19,
    '#FF3881': 22,
    '#FF99AA': 23,
    '#6D482F': 24,
    '#9C6926': 25,
    '#000000': 27,
    '#898D90': 29,
    '#D4D7D9': 30,
    '#FFFFFF': 31
}

access_token_regexp = re.compile(r'"accessToken":"([a-zA-Z0-9\-_]+)"')
expires_in_regexp = re.compile(r'"expiresIn":(\d+)')
csrf_regexp = re.compile(r'<input type="hidden" name="csrf_token" value="(\w+)">')


class CNCOrderClient:
    def __init__(self, session):
        self.session = session
        self.ws = None
        self.logger = logging.getLogger('PlaceNL.cnc')

        self.order_map = None

    async def __aenter__(self):
        self.logger.info("Connecting to Command & Control server...")
        self.ws = await self.session.ws_connect(CNC_WEBSOCKET)
        self.logger.info("Success.")

        asyncio.get_running_loop().create_task(self.ping())

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.ws.close()
        self.ws = None

    async def ping(self):
        await asyncio.sleep(5)

        if not self.ws:
            return

        try:
            await self.ws.send_str(json.dumps({"type": "ping"}))
        except ConnectionResetError:
            self.logger.warning("Could not send ping, websocket closed?")
            self.ws = None

        asyncio.get_running_loop().create_task(self.ping())

    async def receive_orders(self):
        if not self.ws:
            raise Exception("WebSocket not yet initialized! Use async with!")

        await self.ws.send_str(json.dumps({"type": "getmap"}))
        await self.ws.send_str(json.dumps({"type": "brand", "brand": f"PlaceNLpythonV{__version__}"}))

        async for msg in self.ws:
            try:
                data = json.loads(msg.data)
            except:
                continue

            if data['type'] == 'map':
                map_url = f"https://placecz.martinnemi.me/maps/{data['data']}"
                reason = data.get('reason')
                self.logger.info("Loading new map (reason: %s)", reason if reason else "connected to server")
                self.logger.info("Map URL: %s", map_url)

                await self.load_map(map_url)

    async def load_map(self, map_url):
        async with self.session.get(map_url) as resp:
            if resp.status != 200:
                text = await resp.text()
                self.logger.warning("Loading the map failed! Got HTTP response %d. Error:\n%s", resp.status, text)
                return

            data = await resp.read()

            self.order_map = plt.imread(BytesIO(data))
            self.logger.info(
                "Downloaded orders map, image size: %s (dtype: %s)", self.order_map.shape,
                self.order_map.dtype
            )

    async def signal_pixel_drawn(self, row, col, color):
        if not self.ws:
            raise Exception("WebSocket not yet initialized! Use async with!")

        await self.ws.send_str(json.dumps({"type": "placepixel", "x": col, "y": row, "color": color}))
        self.logger.info("Notified CNC server of drawn pixel.")


class RedditPlaceClient:
    def __init__(self, session, username, password, user_agent=None):
        self.session = session
        self.username = username
        self.password = password
        self.user_agent = user_agent if user_agent else DEFAULT_USER_AGENT

        self.access_token = ""
        self.access_token_expire = None
        self.current_canvas = None

        self.logger = logging.getLogger(f'PlaceNL.reddit.{username}')

    async def __aenter__(self):
        self.logger.info("Logging in reddit user %s...", self.username)
        success = await self.login()

        if not success:
            raise Exception("Reddit login was unsuccessful!")

        result = await self.scrape_access_token()

        if not result:
            raise Exception("Could not obtain access token.")

        self.access_token, expires_in = result
        expires = timedelta(seconds=expires_in / 1000)
        self.access_token_expire = datetime.now() + expires

        self.logger.info(
            "Login successful, obtained access token: %s. Expires: %s (%d minutes)", self.access_token,
            self.access_token_expire, expires.total_seconds() // 60
        )

        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.loop = None

    async def login(self) -> bool:
        """Login on reddit.com using the given username and password."""

        # First we have to obtain the form CSRF token
        headers = {
            "User-Agent": self.user_agent
        }

        async with self.session.get(REDDIT_LOGIN_GET, headers=headers) as resp:
            if resp.status != 200:
                self.logger.error(
                    "Could not login to reddit, failed to obtain CSRF token. HTTP status: %d.",
                    resp.status
                )
                return False

            html = await resp.text()
            matches = csrf_regexp.search(html)

            try:
                csrf_token = matches.groups(1)[0]
            except IndexError:
                self.logger.error("Could not login to reddit, failed to obtain CSRF token.")
                return False

        post_data = {
            'csrf_token': csrf_token,
            'username': self.username,
            'password': self.password,
            'dest': "https://www.reddit.com"
        }

        async with self.session.post(REDDIT_LOGIN_POST, data=post_data) as resp:
            if resp.status != 200:
                self.logger.error("Could not login to Reddit! HTTP status %d.", resp.status)
                return False

            cookies = self.session.cookie_jar.filter_cookies(
                "https://www.reddit.com"
            )

            if 'reddit_session' not in cookies:
                self.logger.error("Login unsuccessful! Could not find reddit session cookie.")
                return False

        return True

    async def scrape_access_token(self) -> Optional[tuple[str, int]]:
        """Scrape a few required things from the Reddit Place page.

        We need the `modhash` key (reddit's CSRF protection key) for further
        requests. Furthermore, the Place page contains the websocket URL, which
        we need to obtain updates."""

        async with self.session.get(REDDIT_PLACE_URL) as resp:
            if resp.status != 200:
                return

            data = await resp.text()

            access_token_matches = access_token_regexp.search(data)
            expires_in_matches = expires_in_regexp.search(data)

            if not access_token_matches or not expires_in_matches:
                return

            try:
                access_token = access_token_matches.groups(1)[0]
                expires_in = int(expires_in_matches.groups(1)[0])
            except IndexError:
                self.logger.critical("Could not obtain reddit access token!")
                return

            return access_token, expires_in

    async def refresh_access_token(self):
        result = await self.scrape_access_token()
        if not result:
            self.logger.error("Could not refresh access token, trying again in one minute")
            return False

        self.access_token, expires_in = result
        expires = timedelta(seconds=expires_in / 1000)
        self.access_token_expire = datetime.now() + expires

        self.logger.info(
            "Refreshed access token: %s. Expires: %s (%d minutes)", self.access_token,
            self.access_token_expire, expires.total_seconds() // 60
        )

        return True

    async def load_canvas(self, canvas_id) -> Optional[numpy.ndarray]:
        if datetime.now() > self.access_token_expire:
            result = await self.refresh_access_token()
            if not result:
                return

        headers = {
            "User-Agent": self.user_agent,
            "Origin": "https://hot-potato.reddit.com"
        }

        async with self.session.ws_connect(PLACE_WEBSOCKET, protocols=["graphql-ws"], headers=headers) as ws:
            await ws.send_str(
                json.dumps(
                    {
                        "type": "connection_init",
                        "payload": {
                            "Authorization": f"Bearer {self.access_token}"
                        }
                    }
                )
            )

            await ws.send_str(
                json.dumps(
                    {
                        "id": "1",
                        "type": "start",
                        "payload": {
                            "variables": {
                                "input": {
                                    "channel": {
                                        "teamOwner": "AFD2022",
                                        "category": "CANVAS",
                                        "tag": str(canvas_id)
                                    }
                                },
                            },
                            "extensions": {},
                            "operationName": "replace",
                            "query": GRAPHQL_CANVAS_QUERY,
                        }
                    }
                )
            )

            async for msg in ws:
                try:
                    data = json.loads(msg.data)
                except:
                    self.logger.debug("Couldn't parse websocket msg: %s", msg.data)
                    continue

                name = data.get("payload", {}).get("data", {}).get("subscribe", {}).get("data", {}).get("name")

                if name:
                    self.logger.info("Found current canvas URL: %s", name)
                    await ws.close()

                    random_str = "".join(random.choice(string.ascii_letters) for _ in range(15))

                    async with self.session.get(f"{name}?nocache={random_str}") as resp:
                        if resp.status != 200:
                            text = await resp.text()
                            self.logger.error(
                                "Error obtaining current canvas! HTTP Status: %d. Error:\n%s",
                                resp.status, text
                            )

                            return

                        data = await resp.read()
                        canvas = plt.imread(BytesIO(data))
                        self.logger.info(
                            "Loaded canvas ID %d (image size: %s, dtype: %s)", canvas_id,
                            canvas.shape, canvas.dtype
                        )

                        return canvas

    async def load_full_map(self):
        canvas1 = await self.load_canvas(0)
        canvas2 = await self.load_canvas(1)

        if canvas1 is not None and canvas2 is not None:
            self.current_canvas = numpy.hstack([canvas1, canvas2])

            self.logger.info(
                "Loaded full canvas (shape: %s, dtype: %s)",
                self.current_canvas.shape, self.current_canvas.dtype
            )

    def get_pixels_to_update(self, order_map):
        if self.current_canvas is None:
            self.logger.warning("Current canvas not yet loaded, can't figure out pending pixels...")
            return

        to_update = []

        for row in range(order_map.shape[0]):
            for col in range(order_map.shape[1]):
                # Index 3 is alpha channel, ignore pixels set to transparent
                if order_map[row, col, 3] != 0:
                    if not numpy.array_equal(order_map[row, col, :3], self.current_canvas[row, col, :3]):
                        to_update.append((row, col))

        self.logger.info("Found %d pixels incorrectly colored.", len(to_update))

        # Randomize pixels to ensure we're not trying to update the same pixels again and again
        random.shuffle(to_update)

        return to_update

    async def place_pixel(self, row, col, color) -> float:
        if datetime.now() > self.access_token_expire:
            result = await self.refresh_access_token()

            if not result:
                return 60.0

        self.logger.info("Attempting to place a pixel at (%d, %d) with color %d...", row, col, color)

        headers = {
            'Accept': '*/*',
            'Connection': 'close',
            'authorization': f"Bearer {self.access_token}",
            'Origin': 'https://hot-potato.reddit.com',
            'Referer': 'https://hot-potato.reddit.com/',
            'apollographql-client-name': 'mona-lisa',
            'apollographql-client-version': '0.0.1',
            'Content-Type': 'application/json',
            'User-Agent': self.user_agent,
            'Accept-Encoding': 'gzip, deflate'
        }

        body = {
            'operationName': 'setPixel',
            'variables': {
                'input': {
                    'actionName': 'r/replace:set_pixel',
                    'PixelMessageData': {
                        'coordinate': {
                            'x': str(col % 1000),
                            'y': str(row % 1000),
                        },
                        'colorIndex': str(color),
                        'canvasIndex': str(1 if col > 999 else 0)
                    }
                }
            },
            'query': SET_PIXEL_QUERY
        }

        # Create a new session without any existing cookies
        async with aiohttp.ClientSession() as new_session:
            async with new_session.post(REDDIT_PLACE_SET_PIXEL_URL, headers=headers, json=body) as resp:
                if resp.status != 200:
                    self.logger.error("Error placing pixel! HTTP status %d.", resp.status)
                    text = await resp.text()
                    self.logger.error("%s", text)

                    return 60.0

                try:
                    data = await resp.json()
                    errors = data.get('errors')

                    if errors:
                        self.logger.error("Error placing pixel! Likely placing a new pixel too soon!")
                        next_available = errors[0].get('extensions', {}).get('nextAvailablePixelTs')

                        if next_available:
                            next_dt = datetime.fromtimestamp(float(next_available) / 1000)
                            delta = next_dt - datetime.now()
                            self.logger.info(
                                "Next available possibility: %s (%d seconds)",
                                next_dt, delta.total_seconds()
                            )

                            return delta.total_seconds() + random.randint(5, 60)
                        else:
                            return 300.0  # wait 5 minutes by default
                    else:
                        next_available = float(data['data']['act']['data'][0]['data']['nextAvailablePixelTimestamp'])
                        next_dt = datetime.fromtimestamp(next_available / 1000)
                        delta = next_dt - datetime.now()

                        self.logger.info(
                            "Success! Next pixel will be set at %s (%d seconds)",
                            next_dt, delta.total_seconds()
                        )

                        return delta.total_seconds() + random.randint(5, 60)
                except Exception as e:
                    self.logger.exception("Error placing pixel! Could not read response.")
                    return 60.0


async def cnc_update_task(cnc_client):
    while True:
        await cnc_client.receive_orders()

        cnc_client.logger.warning("Connection to C&C websocket lost, trying again in one minute...")
        await asyncio.sleep(60)


async def reddit_client_task(
        trace_config: aiohttp.TraceConfig, cnc_client: CNCOrderClient,
        username: str, password: str, user_agent: str = None
):
    async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
        async with RedditPlaceClient(session, username, password, user_agent) as place_client:
            delay = 0

            while True:
                if delay > 0:
                    await asyncio.sleep(delay)

                await place_client.load_full_map()

                # Compare current canvas to order map
                to_update = place_client.get_pixels_to_update(cnc_client.order_map)

                if len(to_update) == 0:
                    # No pixels to update, try again in 30 seconds
                    delay = 30
                else:
                    for pixel in to_update:
                        hex = matplotlib.colors.to_hex(cnc_client.order_map[pixel[0], pixel[1], :3]).upper()
                        color_index = COLOR_MAPPINGS[hex]

                        delay = await place_client.place_pixel(pixel[0], pixel[1], color_index)

                        if delay > 60:
                            await cnc_client.signal_pixel_drawn(pixel[0], pixel[1], color_index)
                            break

                        await asyncio.sleep(1)


async def on_request_start(session, ctx, params):
    logging.getLogger('aiohttp.client').debug("Making %s request to %s", params.method, params.url)
    logging.getLogger('aiohttp.client').debug("%s", params.headers)


async def main():
    print("main running...")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u', '--user', nargs=2, action="append",
        help="Reddit username and password. Use this option multiple times to run with multiple users."
    )
    parser.add_argument(
        '-v', '--verbose', action='count', default=0,
        help="Enable verbose output, use multiple times to increase verbosity level."
    )

    args = parser.parse_args()

    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger('PIL').setLevel(logging.INFO)

    if args.verbose > 0:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger('aiohttp.client').setLevel(logging.INFO)

    if args.verbose > 1:
        warnings.filterwarnings("always", category=ResourceWarning)
        asyncio.get_running_loop().set_debug(True)
        logging.getLogger('aiohttp.client').setLevel(logging.DEBUG)

    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(on_request_start)

    while True:
        async with aiohttp.ClientSession(trace_configs=[trace_config]) as cnc_session:
            async with CNCOrderClient(cnc_session) as cnc_client:
                cnc_task = asyncio.create_task(cnc_update_task(cnc_client))

                # Wait a few seconds before starting reddit clients to make sure C&C data has downloaded
                await asyncio.sleep(5)

                tasks = [cnc_task]

                for username, password in args.user:
                    tasks.append(reddit_client_task(trace_config, cnc_client, username, password))

                await asyncio.gather(*tasks)

        # If we reach here, something went wrong, cancel current tasks, and start again
        logger.warning("Lost connection to C&C, restarting...")
        for task in tasks:
            task.cancel()


def run():
    print("run() running...")
    asyncio.run(main())
