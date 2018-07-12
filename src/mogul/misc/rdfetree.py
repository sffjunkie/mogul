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

from lxml import etree
from rdflib.term import URIRef, BNode, Literal
from rdflib.namespace import RDF, is_ncname
from rdflib.exceptions import ParserError, Error
from rdflib.parser import Parser
from xml.sax.xmlreader import InputSource

RDFNS = RDF

class Element(object):
    def __init__(self, parent):
        self.parent = parent

        self.base = ''
        self.language = ''


class ETreeInputSource(InputSource):
    def __init__(self, tree):
        InputSource.__init__(self)
        self.tree = tree

    def read(self):
        return self.tree

class RDFETreeParser(Parser):
    def __init__(self):
        self.tree = None
        self.store = None
        
        self._current = None
        self._namespaces = []
        
        self._tag_re = re.compile('\{([\w\.]+)\}(.+)')
        
        self._parsers = {
            RDFNS.Description: self._parse_description,
            RDFNS.Alt: self._parse_alt,
            RDFNS.Bag: self._parse_bag,
            RDFNS.Seq: self._parse_seq,
            RDFNS.li: self._parse_li,
        }

    def parse(self, source, sink, **args):
        self.tree = source
        self.store = sink
    
        root = Element(None)
        for elem in self.tree:
            self._parse_elem(elem, root)
            
        
    def _parse_elem(self, ee, parent):
        """Parse an etree element
        
        :param ee:     The element to parse
        :type ee:      ETree element
        """
        
        namespaces = ee.nsmap
        
        m = self._tag_re.match(ee.tag)
        ns = m.group(0)
        tag = m.group(1)
        
        if ns not in self._namespaces:
            prefix = ee.nsmap[ns]
            self._namespaces[ns] = prefix
            self.store.bind(prefix, URIRef(ns), override=False)
        
        parser = self._parsers((ns, tag))
        if parser is not None:
            parser()
    
    def _parse_description(self, ee, parent):
        pass
    
    def _parse_alt(self, ee, parent):
        pass
    
    def _parse_bag(self, ee, parent):
        pass
    
    def _parse_seq(self, ee, parent):
        pass
    
    def _parse_li(self, ee, parent):
        pass
    