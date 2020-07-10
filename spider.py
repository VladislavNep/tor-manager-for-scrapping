from tormanager import ConnectionManager
import scrapy
from fake_useragent import UserAgent

class PersonSpider(scrapy.Spider):
    name = "person"
    # recommended settings for scrapy
    custom_settings = {
        "DOWNLOAD_DELAY": 5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "CONCURRENT_REQUESTS": 2,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # initialize tor manager when starting the spider
        self.cm = ConnectionManager('password')

    def start_requests(self):
        _count_req = 0

        urls = [
            'www.exemple.ru/page/1/',
            'www.exemple.ru/page/2/',
        ]

        for url in urls:
            # every 30 requests we will change TOR IP
            _count_req += 1
            if _count_req >= 30:
                self.cm.new_identity()
                _count_req = 0

            # use proxy='127.0.0.1:8118' with Privoxy
            yield scrapy.Request(
                url=url,
                callback=self.parse_info,
                meta=dict(proxy='127.0.0.1:8118'),
                headers={
                    'User-Agent': UserAgent().random,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Referer': 'https://yandex.ru/',
                    'Host': 'www.exemple.ru'
                },

            )

    def parse_info(self, response):
        print('meta: ', response.meta)
        # output the current IP address
        res = requests.get('http://icanhazip.com/', proxies={'http': '127.0.0.1:8118'})
        print(res.text.strip())
