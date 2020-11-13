'''
titan2 - Gemini Protocol Client Transport Library
Copyright (C) 2020  Chris Brousseau

titan2 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

titan2 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with titan2.  If not, see <https://www.gnu.org/licenses/>.
'''

import logging

from .python import urllib
from .globals import *
from .util import normalize_path

logger = logging.getLogger(__name__)

class URL:
  '''
  The URL class negotiates the correct URL based on passed in URL.

  This logic prepares the URL to be passed via the socket connector,
  as well as for the data payload for Gemini.
  '''

  def __init__(self, url, referer_url=None):
    '''
    Construct a protocool-safe URL based on the passed string.
    '''
    self.__input_url = url
    self.__parsed_url = self.__url_constructor(url, referer_url)
    
    logger.debug(
      (f"Recieved url {url} for parsing, ") +
      (f"with referer {referer_url}, " if referer_url else '') + 
      (f"generated gemini url: {self} ") + 
      (f"DEBUG: {self.__parsed_url}")
    )

  def __url_constructor(self, url, referer_url):
    '''
    Constructs a protocol-safe URL based on the passed string.

    If referer_url is included (which should be the constructed
    URL from the last time this ran), the new url is joined onto
    the referer.  This allows the user to pass in paths without a
    hostname.
    '''

    base_url = url
    if referer_url:
      base_url = urllib.parse.urljoin(referer_url, url, False)

    return urllib.parse.urlsplit(base_url, GEMINI_SCHEME, False)

  def __str__(self):
    '''
    Custom logic to re-join the URL into a string
    '''

    # TODO url = 'about:blank', 'example:test' RFC-6694 and RFC-7585
    return ''.join([
      self.protocol(),
      self.host(),
      (f":{self.port()}" if self.port() != GEMINI_PORT else ''),
      self.path(),
      (f"?{self.query()}" if self.query() else '')
    ])

  def path(self):
    '''
    Returns path portion of the url
    URL Schema: scheme://host:port/path?query
    '''

    return normalize_path(self.__parsed_url.path or '')

  def host(self):
    '''
    Returns host portion of the url
    URL Schema: scheme://host:port/path?query
    '''

    return self.__parsed_url.hostname or ''

  def port(self):
    '''
    Returns port portion of the url
    URL Schema: scheme://host:port/path?query
    '''

    try:
      return self.__parsed_url.port or GEMINI_PORT
    except ValueError:
      # https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlsplit
      logger.warn(f"There was an error reading the port from the url. Defaulting to {GEMINI_PORT}")
      return GEMINI_PORT

  def netloc(self):
    '''
    Returns netloc portion of the url, which is the host:port
    URL Schema: scheme://host:port/path?query
    '''

    return self.__parsed_url.netloc

  def protocol(self):
    '''
    Returns scheme portion of the url with the protocol designator "://"
    URL Schema: scheme://host:port/path?query
    '''

    return f"{self.__parsed_url.scheme}://"

  def query(self):
    '''
    Returns query portion of the url
    URL Schema: scheme://host:port/path?query
    '''
    return self.__parsed_url.query