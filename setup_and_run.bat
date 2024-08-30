@echo off

cls
python -m venv venv

call venv\Scripts\activate

pip install scrapy pandas

cd pokescraper

scrapy crawl pokemon_scraper -o ../json\pokemon.json
scrapy crawl ability_scraper -o ../json\abilities.json
scrapy crawl evolution_scraper -o ../json\evo.json

cd ..
python process_pokemon.py

del json\pokemon.json json\abilities.json json\evo.json
rd /s /q json
cls
