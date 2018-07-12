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

import re
import regex
import os.path
from glob import glob
from cgi import escape
import urllib2
import urlparse
import httplib

from lxml import etree

from mogul.misc.nfo import NFOLoader

DEBUG=True

XBMC_SCRAPER_PATH = 'D:\\Program Files\\XBMC\\addons'
USER_SCRAPER_PATH = '%s\\XBMC\\addons' % os.environ['APPDATA']

MOGUL_TMDB_API_KEY = '10514452a82753e376ddbf12949a0c43'
XBMC_TMDB_API_KEY = '57983e31fb435df4df77afb854740ea9'

def _load_from_path(root, scrapers):
    paths = glob(os.path.join(root, 'metadata.*'))
    
    for path in paths:
        addon = load_addon(os.path.join(path, 'addon.xml'))
        if addon is not None:
            addon.path = path
            
            scraper = None
            if addon.extension_points.has_key('xbmc.metadata.scraper.movies'):
                scraper = MovieScraper(addon)
            elif addon.extension_points.has_key('xbmc.metadata.scraper.albums'):
                scraper = AlbumScraper(addon)
            elif addon.extension_points.has_key('xbmc.metadata.scraper.artists'):
                scraper = ArtistScraper(addon)
            elif addon.extension_points.has_key('xbmc.metadata.scraper.library'):
                scraper = ScraperLibrary(addon)
            
            if scraper is not None:
                if scrapers.has_key(scraper.id):
                    if scraper.version > scrapers[scraper.id].version:
                        scrapers[scraper.id] = scraper
                else:
                    scrapers[scraper.id] = scraper

def load_scrapers():
    scrapers = {}
    _load_from_path(XBMC_SCRAPER_PATH, scrapers)
    _load_from_path(USER_SCRAPER_PATH, scrapers)
    return scrapers
        
def load_addon(filename):
    if not os.path.exists(filename):
        return None
    
    try:
        tree = etree.parse(filename)
        root = tree.getroot()
        if root.tag == 'addon':
            addon = Addon()
            
            addon.id = root.attrib['id']
            addon.filename = filename
            addon.name = root.attrib['name']
            addon.version = root.attrib['version']
            addon.provider = root.attrib['provider-name']
    
            for elem in root.iterchildren():
                if elem.tag == 'requires':
                    for imp in elem.iterchildren():
                        if imp.tag == 'import':
                            addon.requires[imp.attrib['addon']] = imp.attrib['version']
                elif elem.tag == 'extension':
                    try:
                        point = elem.attrib['point']
                    except:
                        point = ''

                    try:
                        library = elem.attrib['library']
                    except:
                        library = ''

                    try:
                        language = elem.attrib['language']
                    except:
                        language = ''
                    
                    addon.extension_points[point] = (library, language)

            return addon
        else:
            return None
    except Exception, exc:
        raise


class Addon(object):
    def __init__(self):
        self.path = ''
        self.id = ''
        self.name = ''
        self.version = ''
        self.provider = ''
        
        self.requires = {}
        self.extension_points = {}


class Expression(object):
    def __init__(self, elem):
        self.repeat = (elem.attrib.get('repeat', 'yes') == 'yes')
        self.clear = (elem.attrib.get('clear', 'yes') == 'yes')
        
        v = elem.attrib.get('noclean', '')
        if v != '':
            self.noclean = [int(x) for x in v.split(',')]
        else:
            self.noclean = []

        v = elem.attrib.get('trim', '')            
        if v != '':
            self.trim = [int(x) for x in v.split(',')]
        else:
            self.trim = []
        
        self.cre = None
        self.valid = True
        pattern = elem.text or ''
        if pattern != '':
            #pattern = pattern.replace('<', '\\<')
            #pattern = pattern.replace('>', '\\>')
            #pattern = pattern.replace('-', '\\-')
            try:
                self.cre = regex.compile(elem.text)
            except Exception as exc:
                self.valid = False
                print('Cannot compile %s' % elem.text)

        self.regex = elem.text
                
    def __call__(self, input_, buffers, regexp):
        if not self.valid:
            return buffers
        
        if self.cre is None:
            buffers[0] = input_
            return buffers
        
        print('Using regex %s to scan %s' % (self.regex, input_.replace('\n', ' ')[:255]))
        
        input_matches = regex.search(r'\$\$(\d\d?)', input_)
        if input_matches is not None:
            groups = input_matches.groups()
            for index in range(len(groups)):
                buffer_num = int(groups[index])
                input_ = input_.replace('$$%s' % groups[index], buffers[buffer_num-1], 1)
        
        result = []
        matches = self.cre.findall(input_)
        
        if len(matches) > 0:
            if self.repeat:
                matches_to_process = len(matches)
            else:
                matches_to_process = 1

            fields = ['','','','','','','','','']
            for index in range(matches_to_process):
                
                text = matches[index]
                    
                if index+1 not in self.noclean:
                    text = escape(text)
                        
                if index+1 in self.trim:
                    text = text.strip()
                        
            fields[index] += text
                    
                result.append(fields)
                        
        return result
    

class RegExp(object):
    def __init__(self, elem):
        self.input = elem.attrib.get('input', '$$1')
        self.output = elem.attrib.get('output', '')
        
        dest = elem.attrib.get('dest', '1')
        self.append = False
        if len(dest) > 1 and dest[-1] == '+':
            self.append = True
            dest = dest[:-1]
        self.destination = int(dest)
        
        self.conditional = elem.attrib.get('conditional', '')
                
        self.regexps = []
        self.expression = None
        for child in elem:
            if child.tag == 'expression':
                self.expression = Expression(child)
            elif child.tag == 'RegExp':
                r = RegExp(child)
                self.regexps.append(r)
                
    def __call__(self, buffers):
        for regexp in self.regexps:
            regexp(buffers)
            
        input_ = self.input
        input_matches = regex.search(r'\$\$(\d\d?)', input_)
        if input_matches is not None:
            groups = input_matches.groups()
            for group in groups:
                buffer_num = int(group)
                input_ = input_.replace('$$%d' % buffer_num, buffers[buffer_num-1], 1)
        
        input_matches = regex.search(r'\$INFO\[(\w+)\]', input_)
        if input_matches is not None:
            for item in input_matches.groups():
                input_ = input_.replace('$INFO[%s]' % item, '')

        if input_ != '':                
            expression_matches = self.expression(input_, buffers, self)
            
            if len(expression_matches) > 0:
                result = ''
                
                for match in expression_matches:
                    output = self.output
                    output_matches = regex.search(r'\\(\d\d?)', output)
                    if output_matches is not None:
                        groups = output_matches.groups()
                        for index in range(len(groups)):
                            buffer_num = int(groups[index])
                            output = output.replace('\\%s' % groups[index], match[buffer_num - 1], 1)
                    
                    output_matches = regex.search(r'\$INFO\[(\w+)\]', output)
                    if output_matches is not None:
                        for item in output_matches.groups():
                            if item == 'language':
                                #TODO: Add the actual language somehow
                                # The value is stored in the MyVideos database
                                # Each path has a scraper and a set of settings
                                # in the 'path' table. 
                                output = output.replace('$INFO[%s]' % item, 'en')
            
                    output = output.replace(XBMC_API_KEY, SLITHER_API_KEY)
                    
                    result += '%s\n' % output                
        
                if self.append:
                    result = '%s%s' % (buffers[self.destination-1], result)
                
                tree = etree.fromstring('<output>%s</output>' % result)
            
                for elem in tree.iterfind('.//url[@function]'):
                    function = self.scraper.functions[elem.attrib['function']]
                    if function is not None:
                        buffers[0] = elem.text
                        function(buffers)
            
                buffers[self.destination-1] = result

        
class Function(object):
    def __init__(self, elem):
        self.name = elem.tag
        self.destination = int(elem.attrib.get('dest', '1'))
        
        self.regexps = []
        for child in elem:
            if child.tag == 'RegExp':
                r = RegExp(child)
                self.regexps.append(r)
                
    def __call__(self, buffers):
        for regexp in self.regexps:
            regexp.scraper = self.scraper
            regexp(buffers)

        return buffers[self.destination-1]

class Scraper(object):
    __root__ = 'scraper'
    
    def __init__(self, addon=None):
        self.addon = addon
        self.local_functions = {}
        self.functions = self.Functions(self)
    
        self._load_definition(addon.extension_points[self.__extension_point__][0])

    def id():
        def fget(self):
            return self.addon.id
        
        return locals()
    
    id = property(**id())

    def version():
        def fget(self):
            return self.addon.version
        
        return locals()
    
    version = property(**version())

    class Functions(object):
        def __init__(self, scraper):
            self.scraper = scraper
        
        def __getitem__(self, name):
            if name in self.scraper.local_functions:
                return self.scraper.local_functions[name]
            else:
                #TODO: Add global function support
                return None
            
    def _load_definition(self, filename):
        filename = os.path.join(self.addon.path, filename)
        
        if not os.path.exists(filename):
            raise IOError('Scraper XML definition file not found.')

        tree = etree.parse(filename)
        root = tree.getroot()
        if root.tag != self.__root__:
            raise Exception('File \'%s\' is not a valid %s definition file' % (filename % root.tag))
        
        for elem in root.getchildren():
            f = Function(elem)
            f.scraper = self
            self.local_functions[elem.tag] = f


class MovieScraper(Scraper):
    __extension_point__ = 'xbmc.metadata.scraper.movies'
    
    def __init__(self, addon):
        Scraper.__init__(self, addon)

    def scrape(self, nfo_file='', movie_name=''):
        buffers = ['']*20
        
        url = ''
        if nfo_file != '':
            fp = open(nfo_file, 'r')
            buffers[0] = fp.read(-1)
            fp.close()
            
            if url == '':            
                url = self.local_functions['NfoUrl'](buffers)

        if url == '':
            path, name = os.path.split(nfo_file)
            name, ext = os.path.splitext(name)
            
            match = regex.match(r'([\w\s]+)(\(\d{4}\))$', name)
            if match is not None:
                name, year = match.groups()
            else:
                year = ''

            buffers[0] = name.strip()
            buffers[1] = year                
            search_url = self.local_functions['CreateSearchUrl'](buffers)
            
            if search_url != '':
                try:
                    e = etree.fromstring(search_url)
                    elems = urlparse.urlparse(e.text)
                    fp = urllib2.urlopen()
                    data = fp.read()
                    print(data)
                    
                    buffers[0] = data
                    search_results = self.local_functions['GetSearchResults'](buffers)
                    search_results=search_results
                except urllib2.URLError:
                    pass
        
    

class ArtistScraper(Scraper):
    __extension_point__ = 'xbmc.metadata.scraper.artists'
    
    def __init__(self, addon):
        Scraper.__init__(self, addon)


class AlbumScraper(Scraper):
    __extension_point__ = 'xbmc.metadata.scraper.albums'

    def __init__(self, addon):
        Scraper.__init__(self, addon)


class ScraperLibrary(Scraper):
    __root__ = 'scraperfunctions'
    __extension_point__ = 'xbmc.metadata.scraper.library'
    
    def __init__(self, addon):
        Scraper.__init__(self, addon)

