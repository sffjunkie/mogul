# -*- coding: utf-8 -*-

from mogul.misc.iso_639 import Languages

def test_ISO639_GetItem():
    assert Languages[u'tt'].name == 'Tatar'
    assert Languages[u'tat'].name == 'Tatar'

def test_ISO639():
    assert Languages.iso639_1[u'en'].name == 'English'

def test_ISO639_3():
    assert Languages.iso639_3[u'tat'].name == 'Tatar'
    
def test_ISO639_NativeName():
    assert Languages.iso639_1[u'am'].native_name == u'አማርኛ'
    
def test_ISO639_NativeName_ByIndex():
    assert Languages.iso639_1[u'am'][1] == u'አማርኛ'
    
if __name__ == '__main__':
    test_ISO639_GetItem()
    test_ISO639()
    test_ISO639_3()
    test_ISO639_NativeName()
    test_ISO639_NativeName_ByIndex()
    
