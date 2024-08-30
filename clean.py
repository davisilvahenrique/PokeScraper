import os
import webbrowser

def clean(data_dir):
    if os.path.exists(data_dir):
        for filename in ['pokemon.json', 'abilities.json', 'evo.json']:
            file_path = os.path.join(data_dir, filename)
            if os.path.isfile(file_path):
                print(f"Removing file: {file_path}")
                os.remove(file_path)
        
        if not os.listdir(data_dir):
            print(f"Removing directory: {data_dir}")
            os.rmdir(data_dir)
        else:
            print(f"Directory not empty: {data_dir}")

    processed_file = 'processed_pokemons.json'
    if os.path.exists(processed_file):
        print(f"Opening file: {processed_file}")
        webbrowser.open(f'file://{os.path.abspath(processed_file)}')
    else:
        print(f"File not found: {processed_file}")

if __name__ == "__main__":
    data_dir = 'json'
    clean(data_dir)
