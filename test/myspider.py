import scrapy


class BlogSpider(scrapy.Spider):
    name = 'quote-spdier'
    start_urls = ['https://quotes.toscrape.com']

    def parse(self, response):
        QUOTE_SELECTOR = '.quote'
        TEXT_SELECTOR = '.text::text'
        AUTHOR_SELECTOR = '.author::text'
        ABOUT_SELECTOR = '.author + a::attr("href")'
        TAGS_SELECTOR = '.tags > .tag::text'
        NEXT_SELECTOR = '.next a::attr("href")'

        for quote in response.css(QUOTE_SELECTOR):
            yield {
                'text': quote.css(TEXT_SELECTOR).extract_first(),
                'author': quote.css(AUTHOR_SELECTOR).extract_first(),
                'about': 'https://quotes.toscrape.com' +
                quote.css(ABOUT_SELECTOR).extract_first(),
                'tags': quote.css(TAGS_SELECTOR).extract(),
            }

        next_page = response.css(NEXT_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
            )
