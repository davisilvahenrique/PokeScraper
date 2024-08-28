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

class Pokemon:
    def __init__(self, name, number, url):
        self.name = name
        self.number = number
        self.url = url

class PokemonTree:
    @staticmethod
    def resolve(input, current_name):
        evolutions = []
        
        def extract_evo(card):
            evo_name = card.css('span:nth-of-type(2) > a::text').get()
            evo_number = card.css('span:nth-of-type(2) > small::text').get()
            evo_url = card.css('a::attr(href)').get()
            
            if evo_name and evo_number and evo_url:
                return {
                    'name': evo_name,
                    'number': evo_number,
                    'url': evo_url
                }
            return None
        
        single_evolutions = input.css('.infocard-list-evo > .infocard')
        for card in single_evolutions:
            evo = extract_evo(card)
            if evo:
                evolutions.append(evo)
        
        #ADICIONAR ARRAY DENTRO DA ARRAY PARA SERVIR POR EXEMPLO [EVO 1, [EVO 2, EVO 2, EVO 2, EVO 2], EVO 3, EVO 4]
        multi_evolutions = input.css('.infocard-list-evo .infocard-evo-split .infocard-list-evo')
        for multi in multi_evolutions:
            for card in multi.css('div.infocard'):
                evo = extract_evo(card)
                if evo:
                    evolutions.append(evo)
        
        seen_names = set()
        filtered_evolutions = []
        for evo in evolutions:
            if evo['name'] not in seen_names:
                filtered_evolutions.append(evo)
                seen_names.add(evo['name'])
        
        current_index = None
        for i, evo in enumerate(filtered_evolutions):
            if evo['name'] == current_name:
                current_index = i
                break
        
        if current_index is None or current_index + 1 >= len(filtered_evolutions):
            return None
        
        return filtered_evolutions[current_index + 1]

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
        name = response.css('#main > h1::text').get()
        current_name = name.strip() if name else None
        if not current_name:
            self.logger.warning("Nome do Pokémon não encontrado")
            return

        input_selector = response.css('.infocard-list-evo')
        next_evolution = PokemonTree.resolve(input_selector, current_name)

        evolutions_data = []
        if next_evolution:
            evolutions_data.append({
                'url': self.domain + next_evolution['url'],
                'number': next_evolution['number'],
                'name': next_evolution['name']
            })

        print(evolutions_data)
    
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
                'name': name,
                'height': response.css('.vitals-table > tbody > tr:nth-child(4) > td::text').get(),
                'weight': response.css('.vitals-table > tbody > tr:nth-child(5) > td::text').get(),
                'type 1': response.css('.vitals-table > tbody > tr:nth-child(2) > td > a:nth-child(1)::text').get(),
                'type 2': response.css('.vitals-table > tbody > tr:nth-child(2) > td > a:nth-child(2)::text').get(),
                'evolutions': evolutions_data,
                'abilities': abilities_data
            }
        except Exception as e:
            self.logger.error(f'Erro ao processar {response.url}: {e}')