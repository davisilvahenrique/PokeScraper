from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import sys

def run(spider_name):
    # Carregue as configurações do projeto Scrapy
    process = CrawlerProcess(get_project_settings())

    # Inicie o spider
    process.crawl(spider_name)
    process.start()

if __name__ == "__main__":
    # Verifique se um nome de spider foi fornecido como argumento
    if len(sys.argv) != 2:
        print("Uso: python runSpiders.py <spider_name>")
        sys.exit(1)

    spider_name = sys.argv[1]

    # Liste os spiders disponíveis
    available_spiders = ['ability_scraper', 'evolution_scraper', 'pokemon_scraper']
    if spider_name not in available_spiders:
        print(f"Spider '{spider_name}' não encontrado. Spiders disponíveis: {', '.join(available_spiders)}")
        sys.exit(1)

    run(spider_name)
