VENV_NAME = venv

DATA_DIR = json

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    PYTHON := python3
    PIP := $(VENV_NAME)/bin/pip
    SCRAPY := $(VENV_NAME)/bin/scrapy
    PYTHON_EXEC := $(VENV_NAME)/bin/python
else
    PYTHON := python
    PIP := $(VENV_NAME)/Scripts/pip
    SCRAPY := $(VENV_NAME)/Scripts/scrapy
    PYTHON_EXEC := $(VENV_NAME)/Scripts/python
endif

create_venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_NAME)

install: create_venv
	@echo "Installing dependencies..."
	$(PIP) install scrapy pandas

scrape:
	@echo "Running scrapers..."
	$(SCRAPY) crawl pokemon_scraper -o $(DATA_DIR)/pokemon.json
	$(SCRAPY) crawl ability_scraper -o $(DATA_DIR)/abilities.json
	$(SCRAPY) crawl evolution_scraper -o $(DATA_DIR)/evo.json

process:
	@echo "Processing data..."
	$(PYTHON_EXEC) process_pokemon.py

clean:
	@echo "Cleaning up..."
	$(PYTHON_EXEC) clean.py

mkdir_json:
	@echo "Creating JSON directory if needed..."
	if [ ! -d "$(DATA_DIR)" ]; then mkdir $(DATA_DIR); fi

all: create_venv install mkdir_json scrape process clean

.PHONY: create_venv install scrape process clean mkdir_json all
