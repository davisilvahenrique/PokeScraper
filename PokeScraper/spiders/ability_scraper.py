import scrapy
import re

class AbilityScraper(scrapy.Spider):
    name = 'ability_scraper'
    domain = "https://pokemondb.net"

    start_urls = ["https://pokemondb.net/ability"]

    def parse(self, response):
        abilities = response.css('#abilities > tbody > tr')
        for ability in abilities:
            link = ability.css("td > a::attr(href)").extract_first()
            yield response.follow(self.domain + link, self.parse_ability)

    def parse_ability(self, response):
        html_description = response.css('.grid-row > div > p').get()
        
        desc = self.clean_html(html_description)
        
        yield {
            'url': response.request.url,
            'name': response.css('#main > h1::text').get(),
            'desc': desc
        }

    def clean_html(self, html):
        if not html:
            return ''
        
        html = re.sub(r'<a[^>]*>(.*?)</a>', r'\1', html)
        html = re.sub(r'<[^>]+>', ' ', html)
        html = html.replace('&nbsp;', ' ')
        html = re.sub(r'\s+', ' ', html).strip()
        
        return html