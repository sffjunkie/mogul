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
from datetime import date, timedelta
from collections import defaultdict

from mogul.metadata import MetadataError, MetadataProvider
from mogul.metadata import Movie, Collection, Person

MOGUL_TMDB_API_KEY = '10514452a82753e376ddbf12949a0c43'

class TMDBError(MetadataError):
    pass


class TMDB(MetadataProvider):
    __host__ = 'www.themoviedb.org'
    
    def __init__(self, mock=False):
        super(self, TMDB).__init__()
        
        self.image_configuration = None

        self._mock = mock
        self._methods = {}
        self._methods['append_to'] = ['movie', 'alternative_titles', 'casts',
                               'images', 'keywords', 'releases',
                               'trailers', 'translations',
                               'similar_movies', 'lists',
                               'changes']
    
    def configuration(self):
        prefix = self._url_prefix()
        url = '%s/configuration?api_key=%s' % (prefix, MOGUL_TMDB_API_KEY)
        
        try:
            response = self.read_json(url)
            
            self.image_configuration = response['images'].copy()
        except:
            self.image_configuration = None
            
    def image(self, path, width):
        if self.image_configuration is None:
            self.configuration()
            
        if path[0] != '/':
            path = '/' + path
            
        url = '%s%s%s' % (self.image_configuration['base_url'],
            width, path)
        
        data = self.read_url(url)
        pass

    def movie_search(self, query, **kwargs):
        return self._search('movie', query, **kwargs)

    def movie(self, tmdb_id, language='', append_to_response=[]):
        append_to = [a for a in append_to_response 
                     if a in self._methods['append_to'] and a != 'movie']
        
        try:
            response = self._movie_lookup(tmdb_id,
                                          language=language,
                                          append_to_response=append_to)

            if language == '':
                language = 'en'
            response['lang'] = language

            movie = self._extract_movie(response)
            return movie
        except Exception as exc:
            return None

    def movie_alternative_titles(self, tmdb_id, country='',
                                 append_to_response=[]):
        try:
            response = self._movie_lookup(tmdb_id, 'alternative_titles',
                                          country=country,
                                          append_to_response=append_to_response)
            return response
        except:
            return None

    def movie_casts(self, tmdb_id, append_to_response=[]):
        try:
            response = self._movie_lookup(tmdb_id, 'casts',
                                          append_to_response=append_to_response)
            return response
        except:
            return None

    def movie_images(self, tmdb_id, language='', append_to_response=[]):
        try:
            response = self._movie_lookup(tmdb_id, 'images',
                                          language=language,
                                          append_to_response=append_to_response)
            return response
        except:
            return None

    def movie_keywords(self, tmdb_id, append_to_response=[]):
        try:
            response = self._movie_lookup(tmdb_id, 'keywords',
                                          append_to_response=append_to_response)
            return response
        except:
            return None

    def movie_releases(self, tmdb_id, append_to_response=[]):
        try:
            response = self._movie_lookup(tmdb_id, 'releases',
                                          append_to_response=append_to_response)
            return response
        except:
            return None

    def movie_trailers(self, tmdb_id, append_to_response=[]):
        try:
            response = self._movie_lookup(tmdb_id, 'trailers',
                                          append_to_response=append_to_response)
            return response
        except:
            return None

    def movie_similar_movies(self, tmdb_id, page=-1, language='',
                             append_to_response=[]):
        try:
            response = self._movie_lookup(tmdb_id, 'similar_movies',
                                          page=page,
                                          language=language,
                                          append_to_response=append_to_response)
            return response
        except:
            return None
    
    def collection_search(self, query, **kwargs):
        return self._search('collection', query, **kwargs)

    def collection(self, tmdb_id, language='', append_to_response=[]):
        response = self._collection_lookup(tmdb_id,
                                          language=language,
                                          append_to_response=append_to_response)
                                          
        return response

    def collection_images(self, tmdb_id, language='', append_to_response=[]):
        response = self._collection_lookup(tmdb_id, 'images',
                                          language=language,
                                          append_to_response=append_to_response)
                                          
        return response
    
    def person_search(self, query, **kwargs):
        return self._search('person', query, **kwargs)

    def person(self, tmdb_id, language='', append_to_response=[]):
        response = self._person_lookup(tmdb_id,
                                          language=language,
                                          append_to_response=append_to_response)
                                          
        return response

    def person_credits(self, tmdb_id, language='', append_to_response=[]):
        response = self._person_lookup(tmdb_id, 'credits',
                                       language=language,
                                       append_to_response=append_to_response)
                                          
        return response

    def person_images(self, tmdb_id, language='', append_to_response=[]):
        response = self._person_lookup(tmdb_id, 'images',
                                       language=language,
                                       append_to_response=append_to_response)
                                          
        return response
    
    def person_changes(self, tmdb_id, start_date=None, end_date=None):
        if end_date is None:
            end_date = date.today()
            
        if start_date is None:
            delta = timedelta(days=14)
            start_date = end_date - delta
            
        end = end_date.strftime('%Y-%m-%d')
        start = start_date.strftime('%Y-%m-%d')
                
        response = self._person_lookup(tmdb_id, 'changes',
                                       start_date=start,
                                       end_date=end)
                                          
        return response

    def list_search(self, query, **kwargs):
        return self._search('list', query, **kwargs)

    def list(self, tmdb_id, language='', append_to_response=[]):
        response = self._lookup(tmdb_id, 'list',
                                language=language,
                                append_to_response=append_to_response)
                                          
        return response

    def company_search(self, query, **kwargs):
        return self._search('company', query, **kwargs)

    def company(self, tmdb_id, language='', append_to_response=[]):
        response = self._company_lookup(tmdb_id,
                                        language=language,
                                        append_to_response=append_to_response)
                                          
        return response
        
    def _movie_lookup(self, tmdb_id, path='', **kwargs):
        return self._lookup('movie', tmdb_id, path, **kwargs)
        
    def _collection_lookup(self, tmdb_id, path='', **kwargs):
        return self._lookup('collection', tmdb_id, path, **kwargs)
        
    def _person_lookup(self, tmdb_id, path='', **kwargs):
        return self._lookup('person', tmdb_id, path, **kwargs)
        
    def _company_lookup(self, tmdb_id, path='', **kwargs):
        return self._lookup('company', tmdb_id, path, **kwargs)

    def _lookup(self, root, tmdb_id, path='', **kwargs):
        tmdb_id = str(tmdb_id)
        
        prefix = self._url_prefix()
        if path != '':
            url = '%s/%s/%s/%s?api_key=%s' % (prefix, root, tmdb_id, path,
                MOGUL_TMDB_API_KEY)
        else:
            url = '%s/%s/%s?api_key=%s' % (prefix, root, tmdb_id,
                MOGUL_TMDB_API_KEY)
        
        page = kwargs.get('page', -1)
        if page != -1:
            url += '&page=%d' % page
        
        language = kwargs.get('language', '')
        if language != '':
            url += '&language=%s' % language
        
        country = kwargs.get('country', '')
        if country != '':
            url += '&country=%s' % country
        
        append_to_response = kwargs.get('append_to_response', [])
        if len(append_to_response) > 0:
            url += '&append_to_response=%s' % ','.join(append_to_response)
        
        try:
            return self.read_json(url)
        except:
            return None

    def _search(self, search_type, query, **kwargs):
        prefix = self._url_prefix()
        url = '%s/search/%s?query=%s&api_key=%s' % (prefix, search_type, 
            quote_plus(query), MOGUL_TMDB_API_KEY)

        page = kwargs.get('page', -1)        
        if page != -1:
            url = url + '&page=%d' % page
        
        year = kwargs.get('year', '')
        if year != '':
            url = url + '&year=%s' % str(year)
        
        language = kwargs.get('language', '')
        if language != '':
            url = url + '&language=%s' % language

        if kwargs.get('include_adult', False) == True:        
            url = url + '&include_adult=true'
        
        try:
            return self.read_json(url)
        except:
            return None
    
    def _url_prefix(self):
        if not self._mock:
            return 'http://api.themoviedb.org/3'
        else:
            return 'http://private-3da8-themoviedb.apiary.io/3'

    def _extract_movie(self, response):
        movie = Movie()
        movie['metadata_provider'] = 'tmdb'
        movie['id'] = response['id']
        movie['imdb_id'] = response.get('imdb_id', '')
        
        movie['title'] = defaultdict(list)
        movie['title']['un'] = response['original_title']
        movie['title'][response['lang']] = response['title']
        
        movie['overview'] = response['overview']
        
        movie['adult'] = response['adult']
        movie['collection_id'] = response['belongs_to_collection']
        movie['budget'] = response['budget']
        movie['revenue'] = response['revenue']
        movie['homepage'] = response['homepage']
        
        title_info = response.get('alternative_titles', None)
        if title_info is not None:
            movie['titles'] = self._extract_alternative_titles(title_info)
        
        movie['people'] = {}
        cast_info = response.get('casts', None)
        if cast_info is not None:
            self._extract_cast(cast_info['cast'], movie['people'])
            self._extract_crew(cast_info['crew'], movie['people'])
        
        image_info = response.get('images', None)
        if image_info is not None:
            movie['images'] = self._extract_images(image_info)
        
        keyword_info = response.get('keywords', None)
        if keyword_info is not None:
            movie['keywords'] = self._extract_keywords(keyword_info)
        
        release_info = response.get('releases', None)
        if release_info is not None:
            movie['releases'] = self._extract_releases(release_info)
        
        translation_info = response.get('translations', None)
        if translation_info is not None:
            movie['translations'] = self._extract_translations(translation_info)
        
        return movie

    def _extract_alternative_titles(self, info):
        titles = defaultdict(list)
        for d in info['titles']:
            titles[d['iso_3166_1']].append(d['title'])
        return titles

    def _extract_cast(self, info, people):
        for role in info:
            id_ = role['id']
            
            p = people.get(id_, None)
            if p is None:
                p = Person(id_)
                p.name = role['name']
                p.provider = 'tmdb'
                p.profile_path = role['profile_path']
                people[id_] = p
            
            p.roles['actor'] = role['character']

    def _extract_crew(self, info, people):
        for role in info:
            id_ = role['id']
            
            p = people.get(id_, None)
            if p is None:
                p = Person(id_)
                p.name = role['name']
                p.provider = 'tmdb'
                p.profile_path = role['profile_path']
                people[id_] = p
            
            p.roles[role['job']] = role['department']
    
    def _extract_collection(self, response):
        return response
    
    def _extract_person(self, response):#
        p = Person()
        return p
