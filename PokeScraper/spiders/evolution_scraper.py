import scrapy

class EvolutionScraper(scrapy.Spider):
  name = 'evolution_scraper'
  domain = "https://pokemondb.net"

  start_urls = ["https://pokemondb.net/evolution"]

  def parse(self, response):
    evolutions = response.css('.grid-row > div:nth-child(2) > nav > ul > li')
    for evo in evolutions:
      link = evo.css("a::attr(href)").extract_first()
      yield response.follow(self.domain + link, self.parse_evo)

  def parse_evo(self, response):
    
    evo = response.css('.grid-row > div:nth-child(2) > div > table > tbody > tr')
    for e in evo:
        yield {
            'poke': e.css('td > span > a::text').get(),
            'evo': e.css('td:nth-child(3) > span > a::text').get()
        }   