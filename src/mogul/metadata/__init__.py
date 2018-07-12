# Copyright (c) 2009-2013 Simon Kennedy <code@sffjunkie.co.uk>.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from mogul.jsonrpc.client import RPCClient
from mogul.jsonrpc.message import RPCRequest

class MetadataError(Exception):
    pass


class MetadataProvider(object):
    def __init__(self):
        self._client = RPCClient(self.__host__)

    def read_json(self, url):
        headers = {"Accept": "application/json"}
        data = self.read_url(url, headers)
        response = json.loads(data)
        return response

    def read_url(self, url, headers=None):
        request = RPCRequest(url)
        if headers is not None:
            request.headers = headers
        
        try:
            response = urlopen(request)
            content_types = response.headers.get('Content-Type').split(';')
            data = response.read()
            response.close()
            
            charset = ''
            for ct in content_types:
                if ct.strip().startswith('charset'):
                    charset = ct.split('=')[1]
                    
            if charset == '':
                return data
            else:
                data = data.decode(charset)
                return data
        except URLError as exc:
            raise MetadataError('Unable contact metadata provider: %s' % exc.args[0])


class Movie(dict):
    def title(self, language='un'):
        return self['titles'].get(language, None)


class Collection(dict):
    pass


class Person(dict):
    def __init__(self, id=-1):
        self.id = id
        self.roles = {}


class Cast(dict):
    pass


