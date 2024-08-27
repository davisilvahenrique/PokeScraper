import pandas as pd
import json
import html
import re

def decode_text(text):
    return html.unescape(text)

pokemon_data = pd.read_json('json\\pokemon.json')
abilities_data = pd.read_json('json\\abilities.json')

pokemon_data['number'] = pokemon_data['number'].astype(str).apply(lambda x: x.zfill(4))

pokemon_dict = pokemon_data.set_index('number').T.to_dict('index')
abilities_dict = abilities_data.set_index('url').T.to_dict('index')

def process_pokemon(pokemon):
    number = pokemon['number']
    url = pokemon['url']
    name = pokemon['name']
    
    height_cm = f"{float(pokemon['height'].split(' ')[0].replace('m', '').replace('′', '').replace('″', '')) * 100:.2f} cm"
    weight_kg = f"{float(pokemon['weight'].split(' ')[0].replace('kg', '')):.2f} Kg"
    
    types = []
    types.append(pokemon['type 1'])
    if pokemon['type 2']:
        types.append(pokemon['type 2'])
    
    next_evolutions = pokemon['evolutions']
    # for i in range(1, 15):
    #     evolution = pokemon.get(f'next_evolutions {i}')
    #     if evolution:
    #         evolution_number = evolution.get('number')
    #         if evolution_number:
    #             evolution_number = evolution_number.lstrip('#')
    #             current_evolution_index = int(re.search(r'next_evolutions (\d+)', f'next_evolutions {i}').group(1))
    #             if not any(e['number'] == evolution_number for e in next_evolutions) and (evolution_number != number) and current_evolution_index:
    #                 next_evolutions.append({
    #                     'number': evolution_number,
    #                     'name': evolution['name'],
    #                     'url': evolution['url']
    #                 })

    abilities = pokemon['abilities']
    # for i in range(1, 3):
    #     ability = pokemon.get(f'abilities {i}')
    #     if ability:
    #         description = abilities_dict['desc'].get(ability['url'], 'Descrição não disponível')
    #         description = decode_text(description)
    #         if ability['url'] and ability['name'] and description:
    #             abilities.append({
    #                 'url': ability['url'],
    #                 'name': ability['name'],
    #                 'description': description
    #             })
    
    return {
        'number': number,
        'url': url,
        'name': name,
        'evolutions': next_evolutions,
        'height_cm': height_cm,
        'weight_kg': weight_kg,
        'types': types,
        'abilities': abilities
    }

processed_pokemons = pokemon_data.apply(process_pokemon, axis=1)
result = processed_pokemons.tolist()
result_sorted = sorted(result, key=lambda x: int(x['number']))

with open('json\processed_pokemons.json', 'w', encoding='utf-8') as f:
    json.dump(result_sorted, f, ensure_ascii=False, indent=4)

print("Dados processados salvos em 'processed_pokemons.json'.")
