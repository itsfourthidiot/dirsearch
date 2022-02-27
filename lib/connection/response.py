# -*- coding: utf-8 -*-
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Author: Mauro Soria

from functools import cached_property

from lib.core.settings import CHUNK_SIZE, DEFAULT_ENCODING
from lib.parse.url import parse_path, parse_full_path


class Response(object):
    def __init__(self, response, redirects):
        self.path = parse_path(response.url)
        self.full_path = parse_full_path(response.url)
        self.status = response.status_code
        self.headers = response.headers
        self.redirect = self.headers.get("location")
        self.history = redirects
        self.body = b''

        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            self.body += chunk

        self.content = self.body.decode(response.encoding or DEFAULT_ENCODING, errors="ignore")

    @property
    def type(self):
        return self.headers.get("content-type")

    @cached_property
    def length(self):
        try:
            return int(self.headers.get("content-length"))
        except TypeError:
            return len(self.body)

    def __len__(self):
        return self.length

    def __hash__(self):
        return hash(self.body)

    def __eq__(self, other):
        return (self.status, self.body, self.redirect) == (other.status, other.body, other.redirect)
