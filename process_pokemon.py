import pandas as pd
import json
import html

def decode_text(text):
    return html.unescape(text)

pokemon_data = pd.read_json('json\\pokemon.json')
abilities_data = pd.read_json('json\\abilities.json')
evo_data = pd.read_json('json\\evo.json')

pokemon_data['number'] = pokemon_data['number'].astype(str).apply(lambda x: x.zfill(4))

pokemon_dict = pokemon_data.set_index('number').T.to_dict('index')
abilities_dict = abilities_data.set_index('url').T.to_dict('index')
evo_dict = evo_data.groupby('poke')['evo'].apply(lambda x: list(set(x))).to_dict()

def process_pokemon(pokemon):
    number = pokemon['number']
    url = pokemon['url']
    name = pokemon['name']
    
    height = f"{float(pokemon['height'].split(' ')[0].replace('m', '').replace('′', '').replace('″', '')) * 100:.2f} cm"
    weight = f"{float(pokemon['weight'].split(' ')[0].replace('kg', '')):.2f} Kg"
    
    types = []
    types.append(pokemon['type 1'])
    if pokemon['type 2']:
        types.append(pokemon['type 2'])
    
    evolutions = []
    for evo_name in set(evo_dict.get(name, [])):
        evo_info = pokemon_data[pokemon_data['name'] == evo_name].iloc[0]
        evo_number = evo_info['number']
        evo_url = evo_info['url']
        evolutions.append({
            'number': evo_number,
            'name': evo_name,
            'url': evo_url
        })

    abilities = pokemon.get('abilities', [])
    detailed_abilities = []
    for ability in abilities:
        url = ability['url']
        desc = abilities_dict.get('desc', 'Descrição não disponível').get(url, {})
        detailed_abilities.append({
            'url': url,
            'name': ability['name'],
            'description': decode_text(desc)
        })
    
    return {
        'number': number,
        'url': url,
        'name': name,
        'evolutions': evolutions,
        'height': height,
        'weight': weight,
        'types': types,
        'abilities': detailed_abilities
    }

processed_pokemons = pokemon_data.apply(process_pokemon, axis=1)
result = processed_pokemons.tolist()
result_sorted = sorted(result, key=lambda x: int(x['number']))

with open('processed_pokemons.json', 'w', encoding='utf-8') as f:
    json.dump(result_sorted, f, ensure_ascii=False, indent=4)

print("Dados processados salvos em 'processed_pokemons.json'.")
