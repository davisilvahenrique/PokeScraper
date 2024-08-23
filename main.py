import pandas as pd
import json
import html

def decode_text(text):
    return html.unescape(text)

pokemon_data = pd.read_json('json\\pokemon.json')
abilities_data = pd.read_json('json\\abilities.json')

pokemon_data['number'] = pokemon_data['number'].astype(str).apply(lambda x: x.zfill(4))

pokemon_dict = pokemon_data.set_index('number').T.to_dict('index')
abilities_dict = abilities_data.set_index('url').T.to_dict('index')

eevee_evolutions = []
def process_pokemon(pokemon):
    number = pokemon['number']
    url = pokemon['url']
    name = pokemon['name']
    
    height_cm = f"{float(pokemon['height'].split(' ')[0].replace('m', '').replace('′', '').replace('″', '')) * 100:.2f} cm"
    weight_kg = f"{float(pokemon['weight'].split(' ')[0].replace('kg', '')):.2f} Kg"
    
    type1 = pokemon['type 1']
    type2 = pokemon['type 2']
    
    next_evolutions = []
    for i in range(1, 4):
        evolution_number = pokemon.get(f'next_evolutions_{i}')
        if evolution_number:
            evolution_number = evolution_number.lstrip('#')
            evolution_name = pokemon_dict['name'].get(evolution_number, 'Nome não disponível')
            evolution_url = pokemon_dict['url'].get(evolution_number, 'Url não disponível')
            next_evolutions.append({
                'number': evolution_number,
                'name': evolution_name,
                'url': evolution_url
            })
            if (name == 'Eevee'):
                seen = set()
                unique_evolutions = []
                for pokemon in eevee_evolutions:
                    identifier = (pokemon['number'], pokemon['name'], pokemon['url'])
                    if identifier not in seen:
                        unique_evolutions.append(pokemon)
                        seen.add(identifier)
                next_evolutions += unique_evolutions

    if (pokemon.get('next_evolutions_1') == '#0133' and name != 'Eevee'):
        eevee_evolutions.append({
                'number': number,
                'name': name,
                'url': url
            })

    abilities = []
    for i in range(1, 3):
        ability = pokemon.get(f'abilities {i}')
        if ability:
            description = abilities_dict['desc'].get(ability['url'], 'Descrição não disponível')
            description = decode_text(description)
            abilities.append({
                'url': ability['url'],
                'name': ability['name'],
                'description': description
            })
    
    return {
        'number': number,
        'url': url,
        'name': name,
        'evolutions': next_evolutions,
        'height_cm': height_cm,
        'weight_kg': weight_kg,
        'types': [type1, type2],
        'abilities': abilities
    }

processed_pokemons = pokemon_data.apply(process_pokemon, axis=1)
result = processed_pokemons.tolist()
result_sorted = sorted(result, key=lambda x: int(x['number']))

with open('json\processed_pokemons.json', 'w', encoding='utf-8') as f:
    json.dump(result_sorted, f, ensure_ascii=False, indent=4)

print("Dados processados salvos em 'processed_pokemons.json'.")
