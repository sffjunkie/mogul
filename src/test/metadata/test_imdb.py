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

import os.path

test_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(test_path, 'data')

import bs4

def test_bs4_person_search_results():
    filename = os.path.join(data_path, 'imdb_person_search.html')
    with open(filename) as fp:
        data = fp.read(-1)
    
    soup = bs4.BeautifulSoup(data)
    results = soup.find_all('td', 'result_text')
    
    assert len(results) != 0

    for result in results:
        href = result.find('a')['href']
        print(href)
    pass

def test_bs4_title_search_results():
    filename = os.path.join(data_path, 'imdb_title_search.html')
    with open(filename) as fp:
        data = fp.read(-1)
    
    soup = bs4.BeautifulSoup(data)
    results = soup.find_all('td', 'result_text')
    
    assert len(results) != 0
    
    for result in results:
        href = result.find('a')['href']
        print(href)
    pass

from mogul.metadata.backend.imdb import IMDB

def test_IMDB_parse_html():
    filename = os.path.join(data_path, 'imdb_title_search.html')
    with open(filename) as fp:
        data = fp.read(-1)
    
    i = IMDB()
    soup = i._parse_html(data)
    assert soup is not None

def test_IMDB_extract_id_name():
    filename = os.path.join(data_path, 'imdb_person_search.html')
    with open(filename) as fp:
        data = fp.read(-1)
    
    i = IMDB()
    i._parse_html(data)
    soup = i._parse_html(data)
    name_ids = i._extract_paths_name(soup)
    assert soup is not None
    assert name_ids[0] == '/name/nm0000255'

def test_IMDB_search():
    i = IMDB()
    result = i.person_search('Ben Affleck', exact=True)

if __name__ == '__main__':
    test_bs4_person_search_results()
    test_bs4_title_search_results()
    test_IMDB_parse_html()
    test_IMDB_extract_id_name()
    test_IMDB_search()
