# Copyright (c) 2009-2014 Simon Kennedy <sffjunkie+code@gmail.com>
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

from twisted.internet.protocol import Protocol, ClientFactory

from mogul.json.buffer import JSONBuffer, JSONResultHandler

class XBMCEvent(object):
    pass


class XBMCEventProtocol(Protocol):
    """Listens for notifications from XBMC"""
    
    def __init__(self, event_handler):
        if not callable(event_handler):
            raise ValueError('event_handler must be callable')
        
        self._event_received = event_handler
        
        self._result = JSONResultHandler()
        self._result.add_callback(self.eventReceived)
        self._buffer = JSONBuffer(self._result)
        
    def dataReceived(self, data):
        self._buffer.append(data)

    def eventReceived(self, event):
        e = XBMCEvent()
        e.method = event['method']
        e.params = event['params']['data']
        e.sender = event['params']['sender']
        self._event_received(e)


class XBMCEventFactory(ClientFactory):
    protocol = XBMCEventProtocol

    def __init__(self, event_handler):
        self._event_received = event_handler
        self._protocols = []
        
    def buildProtocol(self, addr):
        p = self.protocol(self._event_received)
        p.factory = self
        self._protocols.append(p)
        return p

    def closeConnections(self):
        for p in self._protocols:
            p.transport.loseConnection()
            