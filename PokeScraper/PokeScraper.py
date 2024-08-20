import scrapy

class PokemonScrapper(scrapy.Spider):
  name = 'pokemon_scrapper'
  domain = "https://pokemondb.net/"

  start_urls = ["https://pokemondb.net/pokedex/all"]

  def parse(self, response):
    pokemons = response.css('#pokedex > tbody > tr')
    for pokemon in pokemons:
      #pokemon = pokemons[0]
      link = pokemon.css("td.cell-name > a::attr(href)").extract_first()
      yield response.follow(self.domain + link, self.parse_pokemon)

  def parse_pokemon(self, response):
    yield {
      'number': response.css('.vitals-table > tbody > tr:nth-child(1) > td > strong::text').get(),
      # 'url': ,
      'name': response.css('#main > h1::text').get(),
      'next_evolutions': response.css('.infocard-list-evo > div:nth-child(3) > span:nth-child(2) > small::text'),
      'next_evolutions': response.css('.infocard-list-evo > div:nth-child(5) > span:nth-child(2) > small::text'),
      'height': response.css('.vitals-table > tbody > tr:nth-child(4) > td::text').get(),
      'weight': response.css('.vitals-table > tbody > tr:nth-child(5) > td::text').get(),
      'type 1': response.css('.vitals-table > tbody > tr:nth-child(2) > td > a:nth-child(1)::text').get(),
      'type 2': response.css('.vitals-table > tbody > tr:nth-child(2) > td > a:nth-child(2)::text').get(),
      'abilities 1': {
        'url': response.css('.vitals-table > tbody > tr:nth-child(6) > td > small > a').href.get(),
        'name': response.css('.vitals-table > tbody > tr:nth-child(6) > td > span > a::text').get(),
        # 'desc': response.css('.vitals-table > tbody > tr:nth-child(6) > td > strong::text').get()
      },
      'abilities 2': {
        'url': response.css('.vitals-table > tbody > tr:nth-child(6) > td > small > a').href.get(),
        'name': response.css('.vitals-table > tbody > tr:nth-child(6) > td > small > a::text').get(),
        # 'desc': response.css('.vitals-table > tbody > tr:nth-child(6) > td > strong::text').get()
      }
    }