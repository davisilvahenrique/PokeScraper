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

class PokemonTree:

    def resolve(input: scrapy.Spider, name: str):
        nextSingle = input.css('div.infocard + span.infocard.infocard-arrow + div.infocard').get()
        ret = []
        if nextSingle is not None:
            evo_name = input.css('span:nth-child(2) > a::text').get()        
            evo_number = input.css('span:nth-child(2) > small::text').get()
            evo_url = input.css('a::attr(href)').get()
            return ret.append([Pokemon(evo_name, evo_number, evo_url)])
        nextMulti = input.css('div.infocard + span.infocard-evo-split > div.infocard-list-evo')
        for one in nextMulti:
            pok = one.css('div.infocard')
            evo_name = pok.css('span:nth-child(2) > a::text').get()        
            evo_number = pok.css('span:nth-child(2) > small::text').get()
            evo_url = pok.css('a::attr(href)').get()
            ret.append(Pokemon(evo_name, evo_number, evo_url))
        # print("####################")
        # # print(name)
        # print(nextMulti)
        return ret
class Pokemon():
    
    def __init__(self, name, number, url):
        self.name = name
        self.number = number
        self.url = url


class PokemonScrapper(scrapy.Spider):
    name = 'pokemon_scrapper'
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

        evolutions = response.css('.infocard-list-evo > div')
        evolutions_data = []
        for evo in evolutions:
            evo_number = evo.css('span:nth-child(2) > small::text').get()
            evo_url = evo.css('a::attr(href)').get()
            evo_name = evo.css('span:nth-child(2) > a::text').get()
            print("####################" + evo_name)
            # print(evo_name)
            # print(evo.css('div.infocard + span.infocard.infocard-arrow + div.infocard').get())
            # print(evo.css('div.infocard + span.infocard-evo-split > div.infocard-list-evo:nth-child(2)').get())
            # print(PokemonTree.resolve(evo, evo_name))
            evolutions_data = PokemonTree.resolve(evo, evo_name)
            p = PokemonTree.resolve(evo, evo_name)[0]
            print({
                    'url': p.url,
                    'number': p.number,
                    'name': p.name
                })
            return
            if evo_number and evo_url and evo_name:
                evolutions_data.append({
                    'url': self.domain + evo_url,
                    'number': evo_number,
                    'name': evo_name
                })

        try:
            yield {
                'number': response.css('.vitals-table > tbody > tr:nth-child(1) > td > strong::text').get(),
                'url': response.request.url,
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