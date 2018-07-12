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

from urllib import quote_plus
import bs4
import regex

from mogul.metadata import MetadataError, MetadataProvider

class IMDBError(MetadataError):
    pass


class IMDB(MetadataProvider):
    def __init__(self):
        MetadataProvider.__init__(self)
        self._name_re = regex.compile('(/name/nm\d+)/')
        self._title_re = regex.compile('(/title/tt\d+)/')
        self._company_re = regex.compile('(/company/co\d+)/')
    
    def movie_search(self, query, **kwargs):
        self._search('tt', query, **kwargs)
    
    def person_search(self, query, **kwargs):
        self._search('nm', query, **kwargs)
    
    def company_search(self, query, **kwargs):
        self._search('co', query, **kwargs)
    
    def tv_show_search(self, query, **kwargs):
        kwargs['ttype'] = 'tv'
        self._search('tt', query, **kwargs)
    
    def tv_episode_search(self, query, **kwargs):
        kwargs['ttype'] = 'ep'
        self._search('tt', query, **kwargs)
    
    def video_game_search(self, query, **kwargs):
        kwargs['ttype'] = 'vg'
        self._search('tt', query, **kwargs)
    
    def _search(self, search_type, query, **kwargs):
        quoted_query = quote_plus(query)
        
        year = kwargs.get('year', None)
        if year is not None:
            quoted_query += '+(%d)'
        
        title_type = kwargs.get('ttype', None)
        if title_type is not None:
            quoted_query += '&ttype=%s' % title_type

        url = '%s?q=%s&s=%s' % (self._url_prefix(), quoted_query, search_type)
        
        exact = kwargs.get('exact', True)
        if exact:
            url += '&exact=true'
            
        data = self.read_url(url)
        soup = self._parse_html(data)
        
        if search_type == 'nm':
            paths = self._extract_paths_name(soup)
        elif search_type == 'tt':
            paths = self._extract_paths_title(soup)
        elif search_type == 'co':
            paths = self._extract_paths_company(soup)
        
        if len(paths) == 0:
            raise IMDBError('No results found for %s' % query)
        
        if exact:
            paths = [paths[0]]
        
        results = [self._read_path(path, search_type) for path in paths]
        return results
    
    def _read_path(self, path, search_type):
        url = 'http://www.imdb.com%s' % path
        data = self.read_url(url)
        soup = self._parse_html(data)
        
        if search_type == 'nm':
            return self._extract_person(soup)
        elif search_type == 'tt':
            return self._extract_title(soup)
        
    def _extract_paths_name(self, soup):
        """Extract IMDB name tokens"""
        
        return self._extract_paths(soup, self._name_re)
        
    def _extract_paths_title(self, soup):
        """Extract IMDB title tokens"""
        
        return self._extract_paths(soup, self._title_re)
        
    def _extract_paths_company(self, soup):
        """Extract IMDB company tokens"""
        
        return self._extract_paths(soup, self._company_re)
    
    def _extract_paths(self, soup, regexp):
        found = []
        results = soup.find_all('td', 'result_text')
        for result in results:
            anchors = result.find_all('a')
            
            for tag in anchors:
                href = tag.get('href', None)
                if href is not None:
                    match = regexp.match(href)
                    if match is not None:
                        found.append(match.groups()[0])
                
        return found
    
    def _extract_person(self, soup):
        pass
    
    def _extract_movie(self, soup):
        pass
    
    def _url_prefix(self):
        return 'http://www.imdb.com/find'
        
    def _parse_html(self, html):
        """Parse the HTML into a form we can use
        
        :param html: The html to parse
        :type html:  string
        :rtype:      ~bs4.BeautifulSoup
        """
        
        return bs4.BeautifulSoup(html)
    