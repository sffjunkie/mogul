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

import os.path

from mogul.misc.nfo import NFOLoader

def filename(name):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', name)

def test_XML_NFO():
    loader = NFOLoader()
    url = filename('xml.nfo').replace('\\', '/')
    loader.load('file:///%s' % url)
    
    assert loader.lookup_id == 'tt0211915'

if __name__ == '__main__':
    test_XML_NFO()
