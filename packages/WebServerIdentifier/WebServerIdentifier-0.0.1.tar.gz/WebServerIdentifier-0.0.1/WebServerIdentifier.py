#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This package identifies web servers.
#    Copyright (C) 2022  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""
This package identifies Web servers using an aggressive
technique based on the maximum size of the URI.

~# python3 WebServerIdentifier.py -d -v -m HEAD identify 127.0.0.1

PythonToolsKit  Copyright (C) 2022  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.


WebServerIdentifier  Copyright (C) 2022  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.

[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:431} Command line arguments parsed.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:443} Identifier built.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:179} New connection built.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:188} URI size: 12261.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:192} Request 1 sent. Get response...
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:295} Request size: 12262, response status: 400.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:310} Servers size: 7.
[*] Response status: 400 for request size: 12262.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:179} New connection built.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:188} URI size: 6097.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:192} Request 2 sent. Get response...
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:295} Request size: 6098, response status: 404.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:310} Servers size: 4.
[*] Response status: 404 for request size: 6098.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:179} New connection built.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:188} URI size: 6131.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:192} Request 3 sent. Get response...
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:295} Request size: 6132, response status: 404.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:310} Servers size: 3.
[*] Response status: 404 for request size: 6132.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:179} New connection built.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:188} URI size: 6132.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:192} Request 4 sent. Get response...
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:295} Request size: 6133, response status: 404.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:310} Servers size: 2.
[*] Response status: 404 for request size: 6133.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:179} New connection built.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:188} URI size: 9186.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:192} Request 5 sent. Get response...
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:295} Request size: 9187, response status: 404.
[2016-06-22 10:15:27] DEBUG    (10) {__main__ - WebServerIdentifier.py:310} Servers size: 1.
[*] Response status: 404 for request size: 9187.
[+] Server header: 'Microsoft-HTTPAPI/2.0'
[+] Web Server found: 'IIS' (request size 12241 pass).

~# python WebServerIdentifier.py -i 1 identify 127.0.0.1:8000

PythonToolsKit  Copyright (C) 2022  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.


WebServerIdentifier  Copyright (C) 2022  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.

[+] Server header: 'SimpleHTTP/0.6 Python/3.10.3'
[+] Web Server found: 'Python' (request size 49140 pass).

~# python WebServerIdentifier.py -m HEAD getmaxuri 127.0.0.1:8000

PythonToolsKit  Copyright (C) 2022  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.


WebServerIdentifier  Copyright (C) 2022  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.

[+] Server header: 'SimpleHTTP/0.6 Python/3.10.3'
[+] Maximum URI length is: 49140, error code: 414 'Request-URI Too Long'

~# python WebServerIdentifier.py -d -v -m HEAD -i 1 getmaxuri 127.0.0.1

PythonToolsKit  Copyright (C) 2022  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.


WebServerIdentifier  Copyright (C) 2022  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.

[2022-04-03 19:10:36] DEBUG    (10) {__main__ - WebServerIdentifier.py:518} Command line arguments parsed.
[2022-04-03 19:10:36] DEBUG    (10) {__main__ - WebServerIdentifier.py:530} Identifier built.
[2022-04-03 19:10:36] DEBUG    (10) {__main__ - WebServerIdentifier.py:286} Get minimum and maximum server URI sizes.
[2022-04-03 19:10:36] DEBUG    (10) {__main__ - WebServerIdentifier.py:310} Start the search for maximum URI length...
[2022-04-03 19:10:36] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:36] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 395735.
[2022-04-03 19:10:36] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 1 sent. Get response...
[2022-04-03 19:10:36] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 395737, response status: 414
[*] Request size: 395737, response code: 414 'Request-URI Too Long'
[2022-04-03 19:10:37] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:37] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 198874.
[2022-04-03 19:10:37] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 2 sent. Get response...
[2022-04-03 19:10:37] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 198876, response status: 414
[*] Request size: 198876, response code: 414 'Request-URI Too Long'
[2022-04-03 19:10:38] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:38] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 100443.
[2022-04-03 19:10:38] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 3 sent. Get response...
[2022-04-03 19:10:38] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 100445, response status: 414
[*] Request size: 100445, response code: 414 'Request-URI Too Long'
[2022-04-03 19:10:39] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:39] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 51228.
[2022-04-03 19:10:39] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 4 sent. Get response...
[2022-04-03 19:10:39] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 51230, response status: 414
[*] Request size: 51230, response code: 414 'Request-URI Too Long'
[2022-04-03 19:10:40] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:40] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 26621.
[2022-04-03 19:10:40] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 5 sent. Get response...
[2022-04-03 19:10:40] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 26623, response status: 414
[*] Request size: 26623, response code: 414 'Request-URI Too Long'
[2022-04-03 19:10:41] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:41] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 14317.
[2022-04-03 19:10:41] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 6 sent. Get response...
[2022-04-03 19:10:41] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 14319, response status: 414
[*] Request size: 14319, response code: 414 'Request-URI Too Long'
[2022-04-03 19:10:42] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:42] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 8165.
[2022-04-03 19:10:42] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 7 sent. Get response...
[2022-04-03 19:10:42] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 8167, response status: 404
[*] Request size: 8167, response code: 404 'Not Found'
[2022-04-03 19:10:43] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:43] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 11241.
[2022-04-03 19:10:43] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 8 sent. Get response...
[2022-04-03 19:10:43] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 11243, response status: 404
[*] Request size: 11243, response code: 404 'Not Found'
[2022-04-03 19:10:44] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:44] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 12779.
[2022-04-03 19:10:44] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 9 sent. Get response...
[2022-04-03 19:10:44] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 12781, response status: 414
[*] Request size: 12781, response code: 414 'Request-URI Too Long'
[2022-04-03 19:10:45] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:45] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 12010.
[2022-04-03 19:10:45] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 10 sent. Get response...
[2022-04-03 19:10:45] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 12012, response status: 404
[*] Request size: 12012, response code: 404 'Not Found'
[2022-04-03 19:10:46] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:46] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 12394.
[2022-04-03 19:10:46] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 11 sent. Get response...
[2022-04-03 19:10:46] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 12396, response status: 414
[*] Request size: 12396, response code: 414 'Request-URI Too Long'
[2022-04-03 19:10:48] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:48] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 12202.
[2022-04-03 19:10:48] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 12 sent. Get response...
[2022-04-03 19:10:48] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 12204, response status: 404
[*] Request size: 12204, response code: 404 'Not Found'
[2022-04-03 19:10:49] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:49] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 12298.
[2022-04-03 19:10:49] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 13 sent. Get response...
[2022-04-03 19:10:49] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 12300, response status: 414
[*] Request size: 12300, response code: 414 'Request-URI Too Long'
[2022-04-03 19:10:50] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:50] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 12250.
[2022-04-03 19:10:50] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 14 sent. Get response...
[2022-04-03 19:10:50] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 12252, response status: 400
[*] Request size: 12252, response code: 400 'Bad Request'
[2022-04-03 19:10:51] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:51] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 12226.
[2022-04-03 19:10:51] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 15 sent. Get response...
[2022-04-03 19:10:51] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 12228, response status: 404
[*] Request size: 12228, response code: 404 'Not Found'
[2022-04-03 19:10:52] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:52] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 12238.
[2022-04-03 19:10:52] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 16 sent. Get response...
[2022-04-03 19:10:52] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 12240, response status: 404
[*] Request size: 12240, response code: 404 'Not Found'
[2022-04-03 19:10:53] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:53] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 12244.
[2022-04-03 19:10:53] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 17 sent. Get response...
[2022-04-03 19:10:53] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 12246, response status: 400
[*] Request size: 12246, response code: 400 'Bad Request'
[2022-04-03 19:10:54] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:54] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 12241.
[2022-04-03 19:10:54] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 18 sent. Get response...
[2022-04-03 19:10:54] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 12243, response status: 400
[*] Request size: 12243, response code: 400 'Bad Request'
[2022-04-03 19:10:55] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:55] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 12240.
[2022-04-03 19:10:55] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 19 sent. Get response...
[2022-04-03 19:10:55] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 12242, response status: 400
[*] Request size: 12242, response code: 400 'Bad Request'
[2022-04-03 19:10:56] DEBUG    (10) {__main__ - WebServerIdentifier.py:261} New connection built.
[2022-04-03 19:10:56] DEBUG    (10) {__main__ - WebServerIdentifier.py:270} URI size: 12239.
[2022-04-03 19:10:56] DEBUG    (10) {__main__ - WebServerIdentifier.py:274} Request 20 sent. Get response...
[2022-04-03 19:10:56] DEBUG    (10) {__main__ - WebServerIdentifier.py:333} Request size: 12241, response status: 404
[*] Request size: 12241, response code: 404 'Not Found'
[2022-04-03 19:10:56] INFO     (20) {__main__ - WebServerIdentifier.py:344} Maximum URI length found: 12241, status: 400, reason: Bad Request.
[+] Server header: 'Microsoft-HTTPAPI/2.0'
[+] Maximum URI length is: 12241, error code: 400 'Bad Request'

~#

>>> from WebServerIdentifier import WebServerIdentifier, _create_unverified_context
>>> identifier = WebServerIdentifier("127.0.0.1", baseuri="/", ssl=True, context=_create_unverified_context(), port=8000, interval=0.5, timeout=2)
>>> identifier = WebServerIdentifier("127.0.0.1")
>>> response = identifier.request()
>>> response.status
404
>>> response.reason
'Not Found'
>>> r = identifier.request(method="HEAD", size=65535)
>>> r.status
414
>>> r.reason
'Request-URI Too Long'
>>> generator = identifier.get_max_URI_size()
>>> size = 0
>>> while size is not None: last_size = size; size, response = next(generator)
...
>>> last_size
12242
>>> generator = identifier.get_max_URI_size(method="HEAD")
>>> generator = identifier.identify_server()
>>> generator = identifier.identify_server(method="HEAD")
>>> response = 0
>>> while response is not None: response, size, servers = next(generator)
...
>>> size
9187
>>> servers
{12241: 'IIS'}
>>> size, name = servers.popitem()
>>> size
12241
>>> name
'IIS'
>>>
"""

__version__ = "0.0.1"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = """
This package identifies Web servers using an aggressive
technique based on the maximum size of the URI.
"""
license = "GPL-3.0 License"
__url__ = "https://github.com/mauricelambert/WebServerIdentifier"

copyright = """
WebServerIdentifier  Copyright (C) 2022  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
__license__ = license
__copyright__ = copyright

__all__ = ["WebServerIdentifier"]

from http.client import HTTPConnection, HTTPSConnection, HTTPResponse
from PythonToolsKit.Arguments import ArgumentParser, verbose
from PythonToolsKit.Random import get_random_strings
from PythonToolsKit.Logs import get_custom_logger
from collections.abc import Callable, Generator
from ssl import _create_unverified_context
from typing import Tuple, Set, List, Dict
from PythonToolsKit.PrintF import printf
from dataclasses import dataclass
from argparse import Namespace
from statistics import median
from functools import partial
from socket import timeout
from logging import Logger
from time import sleep
from enum import Enum

import http.client as httpclient

httpclient._MAXLINE = httpclient._MAXLINE * 2

servers: List[str] = (
    "IIS",
    "Python",
    "Apache",
    "NGINX",
    "Lighttp",
    "OpenLiteSpeed",
    "Caddy",
    "Tomcat",
    "Traefik",
    "WitchServer",
    "Cherokee",
    "H2O",
    "Quark",
)


class WebServerMaxUriSize(Enum):
    IIS0: int = 12284  # 414
    IIS1: int = 12241  # 400
    Python: int = 49140
    Apache: int = 6133
    NGINX: int = 6132
    Lighttp: int = 6095
    OpenLiteSpeed0: int = 24576
    OpenLiteSpeed1: int = 16164
    Caddy: int = 52174
    Tomcat: int = 6091
    Traefik: int = 789458
    WitchServer: int = None  # not defined, unstable
    Cherokee: int = 6098
    H2O: int = 313294
    Quark: int = 2015


class WebServerErrorCode(Enum):
    IIS0: int = 414
    IIS1: int = 400
    Python: int = 414
    Apache: int = 414
    NGINX: int = 414
    Lighttp: int = 431
    OpenLiteSpeed0: int = 414
    OpenLiteSpeed1: int = 0
    OpenLiteSpeed2: int = 503
    Caddy: int = 431
    Tomcat0: int = 0
    Tomcat1: int = 400
    Traefik: int = 431
    WitchServer: int = 0
    Cherokee: int = 413  # No response between 6099 and 7634
    H2O: int = 400
    Quark: int = 2014


@dataclass
class CustomResponse:
    status: int
    reason: str


class WebServerIdentifier:

    """
    This class implements the Web Server Identifier.

    target: The target host (examples: "10.101.10.101:8000", "example.com")
    ssl:    Use HTTPS (SSL, Encryption)
    """

    def __init__(
        self,
        target: str,
        baseuri: str = "/",
        ssl: bool = False,
        interval: float = 0,
        *args,
        **kwargs,
    ):
        self.max_size: int = None
        self.target: str = target
        self.request_counter: int = 0
        self.error_status: int = None
        self.error_reason: str = None
        self.interval: float = interval
        self.last_response: HTTPResponse = None
        self.baseuri: str = baseuri if baseuri[-1] == "/" else (baseuri + "/")
        self.connection_class: Callable = (
            partial(HTTPSConnection, target, *args, **kwargs)
            if ssl
            else partial(HTTPConnection, target, *args, **kwargs)
        )

        self.baseuri_length = len(baseuri)

    def request(self, method: str = "GET", size: int = 0) -> HTTPResponse:

        """
        This function requests the Web Server.

        method: HTTP method to use
        size:   Size of the Query String
        """

        connection = self.connection_class()
        logger_debug("New connection built.")

        uri = self.baseuri
        size = size - self.baseuri_length - 1
        if size > 0:
            uri += "?" + get_random_strings(size, urlsafe=True)
        else:
            size = 0

        logger_debug(f"URI size: {size}.")

        connection.request(method, uri)
        self.request_counter += 1
        logger_debug(f"Request {self.request_counter} sent. Get response...")

        return connection.getresponse()

    @staticmethod
    def get_min_and_max() -> Tuple[int, int]:

        """
        This function returns the minimum and maximum
        size to get a "too long URI error".
        """

        logger_debug("Get minimum and maximum server URI sizes.")
        return (
            min(WebServerMaxUriSize, key=lambda x: (x.value or 65535)),
            max(WebServerMaxUriSize, key=lambda x: (x.value or 0)),
        )

    def get_max_URI_size(
        self, *args, **kwargs
    ) -> Generator[Tuple[int, HTTPResponse]]:

        """
        This function detects the max URI length of the target.
        """

        error_codes: Set[int] = {code.value for code in WebServerErrorCode}
        min_, max_ = self.get_min_and_max()
        min_, max_ = min_.value, max_.value
        interval: int = self.interval
        status: int = 0
        diff: int = 0

        error_status: int = None
        error_reason: str = None

        logger_debug("Start the search for maximum URI length...")

        while diff != 1:
            if interval and diff:
                sleep(interval)

            diff = round((max_ - min_) / 2) or 1
            size = min_ + diff

            try:
                response = self.request(*args, size=size, **kwargs)
            except (ConnectionResetError, TimeoutError, timeout) as e:
                response = CustomResponse(0, e.__class__.__name__)
                logger_debug("Connection error.")

            status = response.status
            if status in error_codes:
                max_ = size
                error_status = status
                error_reason = response.reason
            else:
                min_ = size

            logger_debug(f"Request size: {size}, response status: {status}")
            yield size, response

        if status in error_codes:
            size = size - 1

        self.max_size = size
        self.last_response = response
        self.error_status = error_status
        self.error_reason = error_reason

        logger_info(
            f"Maximum URI length found: {size}, status: "
            f"{error_status}, reason: {error_reason}."
        )

        yield size, None
        yield None, None

    def identify_server(
        self, *args, **kwargs
    ) -> Generator[HTTPResponse, int, Dict[int, str]]:

        """
        This function identifies the target's web server.
        """

        servers: Dict[int, str] = {
            server.value: server.name.rstrip("0123456789")
            for server in WebServerMaxUriSize
            if server.value is not None
        }
        error_codes: Set[int] = {code.value for code in WebServerErrorCode}
        interval: int = self.interval
        response: HTTPResponse = None

        while len(servers) > 1:
            if interval and response:
                sleep(interval)

            middle = round(median(servers))
            response = self.request(*args, size=middle, **kwargs)

            status = response.status
            logger_debug(f"Request size: {middle}, response status: {status}.")

            if status in error_codes:
                servers = {
                    code: name
                    for code, name in servers.items()
                    if code < middle
                }
            else:
                servers = {
                    code: name
                    for code, name in servers.items()
                    if code >= middle
                }

            logger_debug(f"Servers size: {len(servers)}.")
            yield response, middle, servers

        yield None, middle, servers


def parse_args() -> Namespace:

    """
    This function parses command line arguments.
    """

    parser = ArgumentParser(
        description="This package identifies target's web server."
    )

    add_argument = parser.add_argument
    add_argument(
        "action",
        default="identify",
        choices={"identify", "getmaxuri"},
        help=(
            "Identify the target's web server or "
            "get the maximum size of the URI."
        ),
    )
    add_argument(
        "target",
        help="Host targeted (examples: 10.101.10.101:8000, example.com)",
    )
    add_argument(
        "--method",
        "-m",
        default="GET",
        help="HTTP method to request the Web Server",
    )
    add_argument(
        "--baseuri", "-b", default="/", help="Base URI to request the target."
    )
    add_argument("--interval", "-i", type=float, help="Requests interval.")
    add_argument(
        "--ssl", "-s", action="store_true", help="Use HTTPS (SSL, encryption)."
    )
    add_argument(
        "--timeout", "-t", type=int, help="Set timeout for HTTP requests."
    )

    parser.add_verbose(function=partial(printf, state="INFO"))
    parser.add_debug()

    return parser.parse_args()


def get_max_uri_size(
    identifier: WebServerIdentifier, method: str = "GET"
) -> int:

    """
    This function detects the maximum size of the target's URI.
    """

    generator = identifier.get_max_URI_size(method=method)
    size: int = 0

    while size is not None:
        size, response = next(generator)
        last_size = size or last_size

        if response is not None:
            verbose(
                f"Request size: {size}, response code: "
                f"{response.status!r} {response.reason!r}"
            )

            last_response: HTTPResponse = response

    error_status = identifier.error_status
    error_reason = identifier.error_reason
    printf(f"Server header: {last_response.getheader('Server', '')!r}")
    printf(
        f"Maximum URI length is: {last_size}, error code:"
        f" {error_status!r} {error_reason!r}"
    )

    return 0 if error_reason else 1


def identify_server(
    identifier: WebServerIdentifier, method: str = "GET"
) -> int:

    """
    This function prints the probable target's Web Server.
    """

    generator = identifier.identify_server(method=method)
    response: HTTPResponse = 0

    while response is not None:
        response, size, servers = next(generator)

        if response is not None:
            verbose(
                f"Response status: {response.status} for request size: {size}."
            )

            last_response: HTTPResponse = response

    code, name = servers.popitem()
    printf(f"Server header: {last_response.getheader('Server', '')!r}")
    printf(f"Web Server found: {name!r} (request size {code} pass).")

    return 0


def main() -> int:

    """
    This function executes the module from the command line.
    """

    arguments: Namespace = parse_args()
    ssl = arguments.ssl
    action = arguments.action
    timeout = arguments.timeout

    logger_debug("Command line arguments parsed.")

    kwargs = {}
    if ssl:
        kwargs["context"] = _create_unverified_context()

    if timeout:
        kwargs["timeout"] = timeout

    identifier = WebServerIdentifier(
        arguments.target, arguments.baseuri, ssl, arguments.interval, **kwargs
    )
    logger_debug("Identifier built.")

    if action == "getmaxuri":
        return get_max_uri_size(identifier, method=arguments.method)
    elif action == "identify":
        return identify_server(identifier, method=arguments.method)

    return 0


logger: Logger = get_custom_logger(__name__)
logger_debug: Callable = logger.debug
logger_info: Callable = logger.info
logger_warning: Callable = logger.warning
logger_error: Callable = logger.error
logger_critical: Callable = logger.critical

print(copyright)

if __name__ == "__main__":
    exit(main())
