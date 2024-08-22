import scrapy

class AbilityScrapper(scrapy.Spider):
  name = 'ability_scrapper'
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
        'desc': ' '.join(response.css('.grid-row > div > p ::text').getall()).strip()
    }   

class PokemonScrapper(scrapy.Spider):
    name = 'pokemon_scrapper'
    domain = "https://pokemondb.net"
    start_urls = ["https://pokemondb.net/pokedex/all"]

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
    }

    def parse(self, response):
        pokemons = response.css('#pokedex > tbody > tr')
        for pokemon in pokemons:
            link = pokemon.css("td.cell-name > a::attr(href)").extract_first()
            if link:
                yield response.follow(self.domain + link, self.parse_pokemon)
            else:
                self.logger.warning("Link não encontrado para o Pokémon")

        next_page = response.css('a.next::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_pokemon(self, response):
        abilities = response.css('.vitals-table > tbody > tr:nth-child(6) > td')
        abilities_data = []
        for ability in abilities.css('span, small'):
            ability_url = ability.css('a::attr(href)').get()
            ability_name = ability.css('a::text').get()
            if ability_url and ability_name:
                abilities_data.append({
                    'url': self.domain + ability_url,
                    'name': ability_name
                })

        if len(abilities_data) == 1:
            abilities_data.append({
                'url': None,
                'name': None
            })

        abilities_dict = {
            'abilities 1': abilities_data[0] if len(abilities_data) > 0 else {'url': None, 'name': None},
            'abilities 2': abilities_data[1] if len(abilities_data) > 1 else {'url': None, 'name': None},
        }

        try:
            yield {
                'number': response.css('.vitals-table > tbody > tr:nth-child(1) > td > strong::text').get(),
                'url': response.request.url,
                'name': response.css('#main > h1::text').get(),
                'height': response.css('.vitals-table > tbody > tr:nth-child(4) > td::text').get(),
                'weight': response.css('.vitals-table > tbody > tr:nth-child(5) > td::text').get(),
                'type 1': response.css('.vitals-table > tbody > tr:nth-child(2) > td > a:nth-child(1)::text').get(),
                'type 2': response.css('.vitals-table > tbody > tr:nth-child(2) > td > a:nth-child(2)::text').get(),
                'next_evolutions_1': response.css('.infocard-list-evo > div:nth-child(1) > span:nth-child(2) > small::text').get(),
                'next_evolutions_2': response.css('.infocard-list-evo > div:nth-child(3) > span:nth-child(2) > small::text').get(),
                'next_evolutions_3': response.css('.infocard-list-evo > div:nth-child(5) > span:nth-child(2) > small::text').get(),
                **abilities_dict
            }
        except Exception as e:
            self.logger.error(f'Erro ao processar {response.url}: {e}')