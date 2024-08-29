import scrapy

class AbilityScraper(scrapy.Spider):
  name = 'ability_scraper'
  domain = "https://pokemondb.net"

  start_urls = ["https://pokemondb.net/ability"]

  def parse(self, response):
    abilities = response.css('#abilities > tbody > tr')
    for ability in abilities:
      link = ability.css("td > a::attr(href)").extract_first()
      yield response.follow(self.domain + link, self.parse_ability)

  def parse_ability(self, response):
    yield {
        'url': response.request.url,
        'name': response.css('#main > h1::text').get(),
        'desc': ' '.join(response.css('.grid-row > div > p::text').getall()).strip()
    } 

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


class PokemonScraper(scrapy.Spider):
    name = 'pokemon_scraper'
    domain = "https://pokemondb.net"
    start_urls = ["https://pokemondb.net/pokedex/all"]

    def parse(self, response):
        pokemons = response.css('#pokedex > tbody > tr')
        for pokemon in pokemons:
            link = pokemon.css("td.cell-name > a::attr(href)").extract_first()
            if link:
                yield response.follow(self.domain + link, self.parse_pokemon)
            else:
                self.logger.warning("Link não encontrado para o Pokémon")

    def parse_pokemon(self, response):
    
        abilities = response.css('.vitals-table:nth-child(2) > tbody > tr:nth-child(6) > td')
        abilities_data = []
        count = 0
        for ability in abilities.css('span, small'):
            if count >= 3:
                break
            ability_url = ability.css('a::attr(href)').get()
            ability_name = ability.css('a::text').get()
            if ability_url and ability_name:
                abilities_data.append({
                    'url': self.domain + ability_url,
                    'name': ability_name
                })
            count += 1
                
        try:
            yield {
                'number': response.css('.vitals-table > tbody > tr:nth-child(1) > td > strong::text').get(),
                'url': response.request.url,
                'name': response.css('#main > h1::text').get(),
                'height': response.css('.vitals-table > tbody > tr:nth-child(4) > td::text').get(),
                'weight': response.css('.vitals-table > tbody > tr:nth-child(5) > td::text').get(),
                'type 1': response.css('.vitals-table > tbody > tr:nth-child(2) > td > a:nth-child(1)::text').get(),
                'type 2': response.css('.vitals-table > tbody > tr:nth-child(2) > td > a:nth-child(2)::text').get(),
                'abilities': abilities_data
            }
        except Exception as e:
            self.logger.error(f'Erro ao processar {response.url}: {e}')