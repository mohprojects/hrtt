import scrapy


class BlogSpider(scrapy.Spider):
    name = 'news-list-item'
    start_urls = ['https://ilpd.ac.rw/index.php?id=49']

    def parse(self, response):
        ITEM_SELECTOR = 'li'
        TITLE_SELECTOR = 'h2'
        DETAILS_SELECTOR = '.news-info'

        for item in response.css(ITEM_SELECTOR):
            yield {
                'title': item.css(TITLE_SELECTOR).extract_first(),
                'details': item.css(DETAILS_SELECTOR).extract_first(),
            }
