# Projeto PokéScraper

O **PokéScraper** é um projeto que coleta e processa dados de Pokémon usando Scrapy e Python. Ele extrai informações sobre Pokémon, habilidades e evoluções a partir do site [Pokémon Database](https://pokemondb.net), e processa esses dados para gerar um arquivo JSON estruturado.

## Estrutura do Projeto

- **`pokescraper/`**: Contém os spiders do Scrapy e o script de processamento de dados.
  - **`spiders/`**: Diretório com os arquivos dos spiders.
    - **`ability_scraper.py`**: Spider que coleta informações sobre habilidades dos Pokémon.
    - **`evolution_scraper.py`**: Spider que coleta informações sobre as evoluções dos Pokémon.
    - **`pokemon_scraper.py`**: Spider que coleta informações detalhadas sobre cada Pokémon.
  - **`process_pokemon.py`**: Script que processa os dados coletados e gera um arquivo JSON com informações formatadas.

- **`setup_and_run.bat`**: Script em batch que configura o ambiente, executa os spiders e processa os dados.

- **`json/`**: Diretório onde os dados coletados são temporariamente armazenados (criado e removido pelo script `.bat`).

## Requisitos

- **Python 3.x**
- **Scrapy**
- **Pandas**

## Instruções de Uso

1. **Preparação**

   Certifique-se de ter o Python 3.x instalado em seu sistema. O script `.bat` cuidará da criação de um ambiente virtual e instalação das dependências necessárias.

2. **Executar o Projeto**

   Para executar o projeto, basta rodar o arquivo `setup_and_run.bat`. Este script fará o seguinte:

   - Criará um ambiente virtual Python.
   - Ativará o ambiente virtual.
   - Instalará as dependências necessárias (`scrapy` e `pandas`).
   - Executará os spiders para coletar dados de Pokémon, habilidades e evoluções.
   - Processará os dados coletados e gerará um arquivo `processed_pokemons.json` com informações formatadas.
   - Abrirá o arquivo `processed_pokemons.json` no navegador padrão para visualização.
   - Limpará arquivos temporários gerados durante o processo.

   **Para rodar o projeto:**

   1. Navegue até o diretório onde o `setup_and_run.bat` está localizado.
   2. Dê um duplo clique no `setup_and_run.bat` ou execute-o a partir do prompt de comando.

   ```sh
   setup_and_run.bat

3. **Visualização dos Dados**

   Após a execução, o arquivo `processed_pokemons.json` será aberto automaticamente no navegador padrão para visualização.

   **Estrutura do Arquivo setup_and_run.bat**
   ## Estrutura do Arquivo `setup_and_run.bat`

  ```bat
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
```

## Descrição dos Arquivos

- **`pokescraper/spiders/ability_scraper.py`**: Scrapy Spider para coletar informações sobre as habilidades dos Pokémon. Os dados são salvos em `json/abilities.json`.

- **`pokescraper/spiders/evolution_scraper.py`**: Scrapy Spider para coletar informações sobre as evoluções dos Pokémon. Os dados são salvos em `json/evo.json`.

- **`pokescraper/spiders/pokemon_scraper.py`**: Scrapy Spider para coletar informações detalhadas sobre cada Pokémon. Os dados são salvos em `json/pokemon.json`.

- **`pokescraper/process_pokemon.py`**: Script para processar os dados JSON coletados e gerar um arquivo JSON final `processed_pokemons.json` com informações detalhadas sobre cada Pokémon.

- **`setup_and_run.bat`**: Script em batch que automatiza o processo de configuração do ambiente, execução dos spiders e processamento dos dados.

## Notas

- **Codificação UTF-8**: Certifique-se de que o arquivo `.bat` e a janela do console estejam configurados para UTF-8 para suportar caracteres especiais.

- **Navegador**: O arquivo `processed_pokemons.json` será aberto no navegador padrão configurado no sistema.

## Como Usar

1. **Configuração do Ambiente**:
   - Execute o arquivo `setup_and_run.bat` para configurar o ambiente e instalar as dependências necessárias.

2. **Execução dos Spiders**:
   - O script `setup_and_run.bat` também executa automaticamente os spiders para coletar os dados.

3. **Processamento dos Dados**:
   - Após a coleta, o script `process_pokemon.py` será executado para processar os dados e gerar o arquivo final `processed_pokemons.json`.

4. **Visualização dos Dados**:
   - O arquivo `processed_pokemons.json` será aberto no seu navegador padrão para visualização.

