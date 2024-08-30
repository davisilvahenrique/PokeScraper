@echo off
setlocal

chcp 65001

echo Iniciando o processo...

cls
echo Criando e ativando o ambiente virtual...
python -m venv venv
call venv\Scripts\activate

cls
echo Instalando dependências...
pip install scrapy pandas

cd pokescraper

cls
echo Executando o scraper para Pokémon...
scrapy crawl pokemon_scraper -o ../json\pokemon.json

cls
echo Executando o scraper para habilidades...
scrapy crawl ability_scraper -o ../json\abilities.json

cls
echo Executando o scraper para evoluções...
scrapy crawl evolution_scraper -o ../json\evo.json

cd ..

cls
echo Processando os dados...
python process_pokemon.py

cls
echo Limpando arquivos temporários...
del json\pokemon.json json\abilities.json json\evo.json
rd /s /q json

cls
echo Abrindo o arquivo processed_pokemons.json...
start processed_pokemons.json

cls

echo Processo concluído. Pressione qualquer tecla para sair...
pause > nul
