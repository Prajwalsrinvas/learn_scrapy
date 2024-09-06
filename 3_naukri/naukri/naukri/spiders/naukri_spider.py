from urllib.parse import urlencode

import scrapy
from naukri.items import NaukriItem
from scrapy import Request
from scrapy.loader import ItemLoader


class NaukriSpiderSpider(scrapy.Spider):
    name = "naukri_spider"
    allowed_domains = ["naukri.com"]

    def start_requests(self):
        BASE_URL = "https://www.naukri.com/jobapi/v3/search"
        search_keywords = ["python", "web scraping", "scrapy", "web crawling"]
        for search_keyword in search_keywords:
            params = {
                "noOfResults": "100",
                "urlType": "search_by_keyword",
                "searchType": "adv",
                "keyword": search_keyword,
                "pageNo": "1",
                "k": search_keyword,
                "src": "jobsearchDesk",
                "latLong": "",
            }
            headers = {
                "authority": "www.naukri.com",
                "accept": "application/json",
                "accept-language": "en-US,en;q=0.9",
                "appid": "109",
                "content-type": "application/json",
                "systemid": "Naukri",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            }
            url = f"{BASE_URL}/?{urlencode(params)}"
            request = Request(
                url=url,
                method="GET",
                dont_filter=True,
                headers=headers,
                meta={"search_keyword": search_keyword},
            )
            yield request

    def parse(self, response):
        jobs = response.json()["jobDetails"]
        for job in jobs:
            item = ItemLoader(item=NaukriItem(), selector=response)
            item.add_value("search_keyword", response.meta["search_keyword"])
            item.add_value("title", job["title"])
            item.add_value("company_name", job["companyName"])
            item.add_value("job_description", job["jobDescription"])
            item.add_value("date", job["createdDate"])
            item.add_value(
                "location",
                [i["label"] for i in job["placeholders"] if i["type"] == "location"],
            )

            yield item.load_item()
