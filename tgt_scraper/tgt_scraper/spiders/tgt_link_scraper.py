import scrapy

class TgtScraperSpider(scrapy.Spider):
    name = "tgt_scraper"
    allowed_domains = ["thegroundtruthproject.org"]
    start_urls = ["https://thegroundtruthproject.org/category/reports/page/" + str(i) for i in range(1, 85)]

    def parse(self, response):
        links = response.css('h2.entry-title a::attr(href)').getall()
        
        for link in links:
            yield {
                'source_link' :response.url,
                'link': link,
            }