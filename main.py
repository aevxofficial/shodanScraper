from file.scrape.scrape_tool import Scraper
from pprint import pprint

class Main(Scraper):
    def __init__(self):
        super().__init__()
    
    def run(self):
        pprint(self.ScrapeSorgu('html:"buy phone"'))

    
if __name__ == "__main__":
    main = Main()
    main.run()
