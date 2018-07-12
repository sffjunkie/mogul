from mogul.adapter.xbmc.scraper import load_scrapers

def test_Scraper():
    scrapers = load_scrapers()
    tmdb_scraper = scrapers['metadata.themoviedb.org']
    
    nfo = 'D:\\My Documents\\My Videos\\Amelie (2001)\\Amelie (2001).nfo'
    tmdb_scraper.scrape(nfo_file=nfo)
    pass

if __name__ == '__main__':
    test_Scraper()
    