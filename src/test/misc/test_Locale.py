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

from mogul.misc.locale import Locale

def test_Locale():
    l1 = Locale()
    assert l1.language == 'und'
    assert l1.country == 'UND'
    
    l2 = Locale('en')
    assert l2.language == 'eng'
    assert l2.country == 'UND'
    
    l3 = Locale('en', 'GB')
    assert l3.language == 'eng'
    assert l3.country == 'GB'
    
    l4 = Locale('en_GB')
    assert l4.language == 'eng'
    assert l4.country == 'GB'

def test_Locale_Eq():
    l1 = Locale('en', 'GB')
    l2 = Locale('en', 'GB')
    assert l1 == l2

def test_Locale_BestMatch():
    l1 = Locale('en', 'GB')
    l2 = Locale('en')
    l3 = Locale('en', 'GB')
    
    assert l1.best_match(l2, l3) is l3
    
def test_Locale_LanguageInfo():
    l = Locale('en_GB')
    
    li = l.language_info
    assert li.name == 'English'
    
    ci = l.country_info
    assert ci.name == 'United Kingdom'

if __name__ == '__main__':
    test_Locale()
    test_Locale_Eq()
    test_Locale_BestMatch()
    