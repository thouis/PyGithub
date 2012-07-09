# Copyright 2012 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of PyGithub. http://vincent-jacques.net/PyGithub

# PyGithub is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# PyGithub is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with PyGithub.  If not, see <http://www.gnu.org/licenses/>.

import requests
import base64

try:
    import json
except ImportError: #pragma no cover: only for Python 2.5
    import simplejson as json #pragma no cover

import GithubException

class Requester:
    def __init__( self, login_or_token, password ):
        if password is not None:
            login = login_or_token
            self.__authorizationHeader = "Basic " + base64.b64encode( login + ":" + password ).replace( '\n', '' )
        elif login_or_token is not None:
            token = login_or_token
            self.__authorizationHeader = "token " + token
        else:
            self.__authorizationHeader = None
        self.rate_limiting = ( 5000, 5000 )

    def requestAndCheck( self, verb, url, parameters, input ):
        status, headers, output = self.requestRaw( verb, url, parameters, input )
        if status >= 400:
            raise GithubException.GithubException( status, output )
        return headers, output

    def requestRaw( self, verb, url, parameters, input ):
        assert verb in [ "HEAD", "GET", "POST", "PATCH", "PUT", "DELETE" ]

        headers = dict()
        if self.__authorizationHeader is not None:
            headers[ "Authorization" ] = self.__authorizationHeader

        builder = requests.getattr(verb.lower())
        response = builder(url=url, params=parameters, headers=headers)
        status = response.status_code
        headers = response.headers
        output = response.json

        if "x-ratelimit-remaining" in headers and "x-ratelimit-limit" in headers:
            self.rate_limiting = ( int( headers[ "x-ratelimit-remaining" ] ), int( headers[ "x-ratelimit-limit" ] ) )

        # print verb, url, parameters, input, "==>", status, str( headers )[ :30 ], str( output )[ :30 ]
        return status, headers, output

