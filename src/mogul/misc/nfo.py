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

from lxml import etree

try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen

class NFOLoader(object):
    def __init__(self):#
        self._tree = None
    
    def load(self, url):
        ds = urlopen(url)
        data = ds.read()
        ds.close()
        
        try:
            self._tree = self.parse_xml(data)
            return (data, self._tree)
        except:
            return (data, None)
    
    def parse_xml(self, data):
        self._tree = etree.fromstring(data)
        return self._tree
        
    def lookup_id():
        def fget(self):
            if self._tree is not None:
                return self._tree.find('id').text
            else:
                return ''
        
        return locals()
    
    lookup_id = property(**lookup_id())

