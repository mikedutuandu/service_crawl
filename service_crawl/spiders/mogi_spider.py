import scrapy


class MogiSpider(scrapy.Spider):
    def __init__(self):
        super().__init__()
        for i in range(1, 3):
            url = 'https://mogi.vn/mua-nha-dat?cp=' + str(i)
            self.start_urls.append(url)

    name = 'mogi'

    def parse(self, response):
        user_page_links = response.css('.prop-title a.link-overlay')
        yield from response.follow_all(user_page_links, self.parse_user)

    def parse_user(self, response):
        def extract_with_css_name(query1, query2):
            name = response.css(query1).get(default='').strip()
            if name == "":
                name = response.css(query2).get(default='').strip()
            return name

        def extract_with_css_phone(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css_name('.agent-name a::text', '.agent-name::text'),
            'phone': extract_with_css_phone('.agent-contact a::text'),
        }
