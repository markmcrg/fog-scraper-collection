import scrapy
import pandas as pd
import re

class TgtArticleScraperSpider(scrapy.Spider):
    name = "tgt_article_scraper"
    allowed_domains = ["thegroundtruthproject.org"]

    def start_requests(self):
        # Retrieve the file argument passed
        file = getattr(self, 'file', None)
        if file:
            try:
                # Read csv into a dataframe and loop over the domain_url column
                df = pd.read_csv(file)
                for link in df['link']:
                    yield scrapy.Request(url=link, callback=self.parse)
            except FileNotFoundError:
                print("File not found")
        else:
            print("File not specified")

    def parse(self, response):
        title = response.css("h2.entry-title::text").get()
        author = response.css("a.author-link::text").get()
        author_href = response.css("a.author-link::attr(href)").get()
        article_content = response.css("div.entry-content.is_article *::text").extract()

        article_content = " ".join(article_content)
        
        yield {
            'article_link' :response.url,
            "title": title,
            "author": author,
            "author_link": author_href,
            "article_content": article_content
        }
