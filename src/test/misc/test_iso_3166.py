# -*- coding: utf-8 -*-

from mogul.misc.iso_3166 import Countries

def test_ISO3166_GetItem():
    assert Countries[u'en'].name == 'English'

if __name__ == '__main__':
    test_ISO3166_GetItem()

