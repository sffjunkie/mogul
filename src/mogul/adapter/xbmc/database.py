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

from sqlalchemy import create_engine, MetaData

class XBMCDatabase(object):
    def __init__(self, connect_string=''):
        self._connect_string = connect_string
        self.connection = None
        
    def connect(self):    
        self.engine = create_engine(self._connect_string)
        self.connection = self.engine.connect()
        
        self.metadata = MetaData(bind=self.connection)
        self.metadata.reflect()

        result = self.connection.execute('select * from version')
        row = result.fetchone()
        self.version = row.idVersion
        

class MusicDatabase(XBMCDatabase):
    def __init__(self, connect_string=''):
        XBMCDatabase.__init__(self, connect_string)
        
    def test(self):
        pass


class VideoDatabase(XBMCDatabase):
    def __init__(self, connect_string=''):
        XBMCDatabase.__init__(self, connect_string)
        
    def test(self):
        pass
