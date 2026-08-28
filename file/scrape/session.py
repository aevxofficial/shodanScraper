from curl_cffi import Session
import json
from fake_useragent import UserAgent

class ScraperSession:
    def __init__(self):
        self.session = Session(impersonate="chrome110",)
        self.config = json.load(open("file/scrape/config.json"))
        self.Config()
        
    def Config(self):

        self.session.headers.update({
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding":"gzip, deflate, br, zstd",
            "sec-ch-ua-platform-version":"10.0.0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest":"document",
            "sec-fetch-mode":"navigate",
            "sec-fetch-site":"same-origin",
            "User-Agent": UserAgent().random
        })

        self.session.cookies.update(self.config["cookies"])