from async_scraper import AsyncScraper
import bs4


class MyScraper(AsyncScraper):
    def parse(self, html):
        soup = bs4.BeautifulSoup(html, 'html.parser')
        return soup.title.string


if __name__ == '__main__':
    urls = [f'https://www.windguru.cz/{spot_id}' for spot_id in range(50, 60)]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0'}

    scraper = MyScraper(urls, requests_per_second=5, concurrent_requests=3, ignore_codes=[404], headers=headers)
    all_data = scraper.run()

    for data in all_data:
        print(data)
