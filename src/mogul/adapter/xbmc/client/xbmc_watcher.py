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

from twisted.internet.protocol import Protocol, ReconnectingClientFactory

from xbmc_event import XBMCEvent


class XBMCWatcherFactory(ReconnectingClientFactory):
    """XBMCWatcherFactory monitors a connection to an XBMC instance"""
    
    protocol = Protocol

    def __init__(self, event_handler):
        self.factor = 1.6180339887498948
        self._event_received = event_handler
        self._protocols = []
        self._connected = False
        
    def buildProtocol(self, addr):
        p = self.protocol()
        p.factory = self

        if not self._connected:
            e = XBMCEvent()
            e.method = 'Watcher.Connection'
            e.params = {'connected': True}
            e.sender = 'XBMCWatcher'
            self._event_received(e)
            self._connected = True
        
        self._protocols.append(p)
        return p

    def clientConnectionFailed(self, connector, reason):
        if self._connected:
            e = XBMCEvent()
            e.method = 'Watcher.Connection'
            e.params = {'connected': False}
            e.sender = 'XBMCWatcher'
            self._event_received(e)
            self._connected = False
        
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def clientConnectionLost(self, connector, reason):
        if self._connected:
            e = XBMCEvent()
            e.method = 'Watcher.Connection'
            e.params = {'connected': False}
            e.sender = 'XBMCWatcher'
            self._event_received(e)
            self._connected = False
        
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
        