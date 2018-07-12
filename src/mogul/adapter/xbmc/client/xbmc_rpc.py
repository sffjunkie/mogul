# Copyright (c) 2014 Simon Kennedy <sffjunkie+code@gmail.com>.

import logging

from mogul.json.message import Request
from mogul.json.aio import AIOClient

class XBMCRPCError(Exception):
    pass


class XBMCRPC(AIOClient):
    def __init__(self, reactor, host='127.0.0.1', port=8080, username='',
                 password='', debug=False):
        txClient.__init__(self, reactor, host, port, username, password)

        self.title = 'XBMC RPC'

        self._available_commands = {}
        
        self._active_commands = {
            'Available': False,
            'ActivePlayers': False,
            'ActiveItem': False,
            'GetProperties': False,
        }
        
        self.players = {
            'audio': -1,
            'video': -1,
            'picture': -1
        }
        
        self.debug = debug
        
        self._configure_logging()

    def connect(self):
        def ok(msg):
            self._available_commands.clear()
            for name, value in msg.result['methods'].items():
                self._available_commands[name] = value
            
            return True
        
        def fail(response):
            self._available_commands.clear()
            return False
            
        d = Deferred()
        d.addCallback(ok)
        r = Request('JSONRPC.Introspect')
        self.request(r, d)
        
        return d

    def _configure_logging(self):
        self.logger = logging.getLogger('xbmc')
        if self.debug == True:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        
        # Create formatter overriding ``datefmt`` to remove milliseconds from stream output
        sf = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        sh = logging.StreamHandler()
        sh.setFormatter(sf)
        self.logger.addHandler(sh)
    
    def active_players(self):
        def ok(response):
            if len(response.result) != 0:
                for player in response.result:
                    if self.players[player['type']] == -1:
                        self.logger.debug('%s: Player %s has started' % (self.title, player['type']))
                        
                    self.players[player['type']] = player['playerid']
            else:
                if self.players['audio'] != -1:
                    self.logger.debug('%s: audio player stopped' % self.title)
                self.players['audio'] = -1

                if self.players['video'] != -1:
                    self.logger.debug('%s: video player stopped' % self.title)
                self.players['video'] = -1

                if self.players['picture'] != -1:
                    self.logger.debug('%s: picture player stopped' % self.title)
                self.players['picture'] = -1

            self._active_commands['ActivePlsayers'] = False
            return False
        
        def fail(response):
            self.players['audio'] = -1
            self.players['video'] = -1
            self.players['picture'] = -1
            self.logger.debug('%s: XBMC has probably died' % self.title)
            self._active_commands['ActivePlayers'] = False
            return False

        if not self._active_commands['ActivePlayers']:
            self._active_commands['ActivePlayers'] = True
            
            d = Deferred()
            d.addCallback(ok)
            d.addErrback(fail)
            r = Request('Player.GetActivePlayers')
            self.request(r, d)
        
            return d
            
    def active_items(self):
        for player_id in self.players.values():
            if player_id != -1:
                self.active_item(player_id)
    
    def active_item(self, player_id):
        def ok(response):
            self._active_commands['ActiveItem'] = False
            return response
        
        def fail(response):
            self._active_commands['ActiveItem'] = False
            return False
        
        if not self._active_commands['ActiveItem']:
            self._active_commands['ActiveItem'] = True
    
            d = Deferred()
            d.addCallback(ok)
            d.addErrback(fail)
            r = Request('Player.GetItem', playerid=player_id)
            self.request(r, d)
            
            return d
        
    def get_properties(self, properties):
        def ok(response):
            self._active_commands['GetProperties'] = False
            return response
        
        def fail(response):
            self._active_commands['GetProperties'] = False
            return False
        
        if not self._active_commands['GetProperties']:
            self._active_commands['GetProperties'] = True
    
            d = Deferred()
            d.addCallback(ok)
            d.addErrback(fail)
            r = Request('Application.GetProperties', properties=properties)
            self.request(r, d)
            
            return d

    class _Command(object):
        def __init__(self, name, info):
            self._name = name
            self._info = info
        
        def __call__(self, *args, **kwargs):
            def ok(msg):
                return msg
                
            def fail(error):
                return error
            
            d = Deferred()
            r = Request(self.name, kwargs)
            self.request(r, d)
            d.addCallback(ok)
            d.addErrback(fail)
        