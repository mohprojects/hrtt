import scrapy


class BlogSpider(scrapy.Spider):
    name = 'news'
    start_urls = ['https://www.nrs.gov.rw/index.php?id=95']

    def parse(self, response):
        ITEM_SELECTOR = '.content-news'
        URL_SELECTOR = 'a::attr("href")'
        TITLE_SELECTOR = 'a::attr("title")'
        IMAGE_SELECTOR = '.img a img::attr("src")'
        DETAILS_SELECTOR = 'p'
        DATETIME_SELECTOR = '.extra time::attr("datetime")'
        NEXT_SELECTOR = '.next a::attr("href")'

        for item in response.css(ITEM_SELECTOR):
            yield {
                'url': item.css(URL_SELECTOR).extract_first(),
                'title': item.css(TITLE_SELECTOR).extract_first(),
                'image': item.css(IMAGE_SELECTOR).extract_first(),
                'details': item.css(DETAILS_SELECTOR).extract_first(),
                'datetime': item.css(DATETIME_SELECTOR).extract_first(),
            }

        next_page = response.css(NEXT_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
            )
