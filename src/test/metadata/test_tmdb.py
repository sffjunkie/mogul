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

from mogul.metadata.backend.tmdb import TMDB

def test_TMDB_Configuration():
    t = TMDB(mock=True)
    t.configuration()

def test_TMDB_Movie():
    t = TMDB(mock=True)
    result = t.movie(387)
    assert result is not None

def test_TMDB_MovieLanguage():
    t = TMDB(mock=True)
    result = t.movie(387, language='fr')
    assert result is not None

def test_TMDB_MovieImages():
    t = TMDB(mock=True)
    result = t.movie_images(387)
    file_path = result['posters'][0]['file_path']
    _image = t.image(file_path, 'w500')

def test_TMDB_MovieAppendTo():
    t = TMDB(mock=True)
    extra_responses = ['alternative_titles', 'casts', 'images', 'keywords',
                       'releases', 'trailers', 'similar_movies', 'lists',
                       'changes']
    result = t.movie(387, append_to_response=extra_responses)
    assert result is not None

def test_TMDB_MovieSearch():
    t = TMDB(mock=True)
    result = t.movie_search('Das Boot', language='en')
    assert result is not None

def test_TMDB_Collection():
    t = TMDB(mock=True)
    result = t.collection(1570)
    assert result is not None

def test_TMDB_CollectionSearch():
    t = TMDB(mock=True)
    result = t.collection_search('Die Hard')
    assert result is not None

if __name__ == '__main__':
    #test_TMDB_Configuration()
    #test_TMDB_Movie()
    #test_TMDB_MovieLanguage()
    test_TMDB_MovieAppendTo()
    #test_TMDB_MovieImages()
    #test_TMDB_MovieSearch()
    #test_TMDB_Collection()
    #test_TMDB_CollectionSearch()
