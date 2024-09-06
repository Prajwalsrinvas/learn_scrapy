import scrapy
from scrapy import FormRequest, Request


class QuotesLoginSpiderSpider(scrapy.Spider):
    name = "quotes_login_spider"
    allowed_domains = ["quotes.toscrape.com"]

    def start_requests(self):
        url = "http://quotes.toscrape.com/login"
        yield Request(url, callback=self.parse_login)

    def parse_login(self, response):
        self.log(
            f"""Form with hidden input field, contains CSRF token value: {response.xpath('//input[@type="hidden"]').get()}"""
        )
        data = {"username": "test_username", "password": "test_password"}
        # https://docs.scrapy.org/en/latest/topics/request-response.html#topics-request-response-ref-request-userlogin
        request = FormRequest.from_response(response, formdata=data)
        self.log(
            f"Request Body: {request.body}"
        )  # notice the CSRF token being automatically added
