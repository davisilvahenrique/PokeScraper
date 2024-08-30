# Projeto PokéScraper

O **PokéScraper** é um projeto que coleta e processa dados de Pokémon usando Scrapy e Python. Ele extrai informações sobre Pokémon, habilidades e evoluções a partir do site [Pokémon Database](https://pokemondb.net), e processa esses dados para gerar um arquivo JSON estruturado.

## Estrutura do Projeto

- **`pokescraper/`**: Contém os spiders do Scrapy e o script de processamento de dados.
  - **`spiders/`**: Diretório com os arquivos dos spiders.
    - **`ability_scraper.py`**: Spider que coleta informações sobre habilidades dos Pokémon.
    - **`evolution_scraper.py`**: Spider que coleta informações sobre as evoluções dos Pokémon.
    - **`pokemon_scraper.py`**: Spider que coleta informações detalhadas sobre cada Pokémon.
  - **`process_pokemon.py`**: Script que processa os dados coletados e gera um arquivo JSON com informações formatadas.

- **`Makefile`**: Arquivo que configura o ambiente, executa os spiders e processa os dados.

- **`json/`**: Diretório onde os dados coletados são temporariamente armazenados (criado e removido pelo `Makefile`).

- **`clean.py`**: Script que remove arquivos temporários e abre o arquivo de dados processados no navegador.

## Requisitos

- **Python 3.x**
- **Scrapy**
- **Pandas**
- **make** (para executar o `Makefile`)

## Instruções de Uso

1. **Preparação**

   Certifique-se de ter o Python 3.x e `make` instalados em seu sistema. O `Makefile` cuidará da criação de um ambiente virtual e instalação das dependências necessárias.

2. **Executar o Projeto**

   Para executar o projeto, use o comando `make` para seguir as seguintes etapas:

   - Criar um ambiente virtual Python.
   - Ativar o ambiente virtual e instalar as dependências necessárias (`scrapy` e `pandas`).
   - Executar os spiders para coletar dados de Pokémon, habilidades e evoluções.
   - Processar os dados coletados e gerar um arquivo `processed_pokemons.json` com informações formatadas.
   - Limpar arquivos temporários gerados durante o processo.

**Para rodar o projeto:**

   1. Navegue até o diretório onde o `Makefile` está localizado.
   2. Execute o comando:

   ```sh
   make all

3. **Visualização dos Dados**

   Após a execução, o arquivo `processed_pokemons.json` será aberto automaticamente no navegador padrão para visualização.

## Descrição dos Arquivos

- **`spiders/ability_scraper.py`**: Scrapy Spider para coletar informações sobre as habilidades dos Pokémon. Os dados são salvos em `json/abilities.json`.

- **`spiders/evolution_scraper.py`**: Scrapy Spider para coletar informações sobre as evoluções dos Pokémon. Os dados são salvos em `json/evo.json`.

- **`spiders/pokemon_scraper.py`**: Scrapy Spider para coletar informações detalhadas sobre cada Pokémon. Os dados são salvos em `json/pokemon.json`.

- **`process_pokemon.py`**: Script para processar os dados JSON coletados e gerar um arquivo JSON final `processed_pokemons.json` com informações detalhadas sobre cada Pokémon.

- **`clean.py`**: Script para remover arquivos temporários e abrir o arquivo processed_pokemons.json no navegador.

- **`Makefile`**: Arquivo que automatiza o processo de configuração do ambiente, execução dos spiders e processamento dos dados.

## Notas

- **Codificação UTF-8**: Certifique-se de que seu terminal ou prompt de comando esteja configurado para UTF-8 para suportar caracteres especiais.

