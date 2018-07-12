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
from lxml import etree
import rdflib
from mogul.misc.rdfetree import ETreeInputSource

NSMAP = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
}

def filename(name):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', name)

def test_Empty_RDF():
    tree = etree.parse(filename('empty.xmp'))
    root = tree.xpath('rdf:RDF', namespaces=NSMAP)
    
    g = rdflib.Graph()
    g.parse(data=etree.tostring(root[0]), format='application/rdf+xml')
    assert g is not None

def test_ETree_Plugin():
    rdflib.plugin.register('etree', rdflib.parser.Parser, 'mogul.misc.rdfetree', 'RDFETreeParser')

    tree = etree.parse(filename('empty.xmp'))
    root = tree.xpath('rdf:RDF', namespaces=NSMAP)
    
    source = ETreeInputSource(root)
    
    g = rdflib.Graph()
    g.parse(source=source, format='etree')


if __name__ == '__main__':
    test_Empty_RDF()
    test_ETree_Plugin()
    