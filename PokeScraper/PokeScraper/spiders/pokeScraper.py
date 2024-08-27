import scrapy
import re

class AbilityScrapper(scrapy.Spider):
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

class PokemonTree:
    
    def resolve(input: scrapy.Spider, url: str):
        url = re.search(r'https://pokemondb\.net/pokedex/([^/]+)', url).group(1)
        url = re.sub(r'[^a-zA-Z]', '', url).lower()
        ret = []
        names = input.css('span:nth-child(2) > a::text').getall()
        normal_names = [re.sub(r'[^a-zA-Z]', '', name).lower() for name in names]
        print(normal_names)
        elements_with_name = 1
        index = elements_with_name(url) if url in elements_with_name else -1
        if index != -1:
            nextSingle = input.css('div.infocard + span.infocard.infocard-arrow + div.infocard')
            if nextSingle is None:
                evo_name = input.css('span:nth-child(2) > a::text').get()        
                evo_number = input.css('span:nth-child(2) > small::text').get()
                evo_url = input.css('a::attr(href)').get()
                ret.append(Pokemon(evo_name, evo_number, evo_url))
                return ret
            nextMulti = input.css('div.infocard + span.infocard-evo-split > div.infocard-list-evo')
            for one in nextMulti:
                pok = one.css('div.infocard')
                evo_name = pok.css('span:nth-child(2) > a::text').get()        
                evo_number = pok.css('span:nth-child(2) > small::text').get()
                evo_url = pok.css('a::attr(href)').get()
                ret.append(Pokemon(evo_name, evo_number, evo_url))
        return ret
    
class Pokemon():
    
    def __init__(self, name, number, url):
        self.name = name
        self.number = number
        self.url = url

class PokemonScrapper(scrapy.Spider):
    name = 'pokemon_scraper'
    domain = "https://pokemondb.net"
    start_urls = ["https://pokemondb.net/pokedex/all"]

    def parse(self, response):
        pokemons = response.css('#pokedex > tbody > tr')
        for pokemon in [pokemons[162]]:
            link = pokemon.css("td.cell-name > a::attr(href)").extract_first()
            if link:
                yield response.follow(self.domain + link, self.parse_pokemon)
            else:
                self.logger.warning("Link não encontrado para o Pokémon")

    def parse_pokemon(self, response):

        evolutions_data = []
        url = response.request.url,
        evolutions = PokemonTree.resolve(response.css('.infocard-list-evo'), url[0])
        for one in range(len(evolutions)):
            p = evolutions[one]
            if p:
                evolutions_data.append({
                    'url': self.domain + p.url,
                    'number': p.number,
                    'name': p.name
                })
        print(evolutions_data)
        return

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
                'url': url,
                'name': response.css('#main > h1::text').get(),
                'height': response.css('.vitals-table > tbody > tr:nth-child(4) > td::text').get(),
                'weight': response.css('.vitals-table > tbody > tr:nth-child(5) > td::text').get(),
                'type 1': response.css('.vitals-table > tbody > tr:nth-child(2) > td > a:nth-child(1)::text').get(),
                'type 2': response.css('.vitals-table > tbody > tr:nth-child(2) > td > a:nth-child(2)::text').get(),
                'evolutions': evolutions_data,
                'abilities': abilities_data
            }
        except Exception as e:
            self.logger.error(f'Erro ao processar {response.url}: {e}')