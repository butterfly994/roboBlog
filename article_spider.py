import scrapy
from bs4 import BeautifulSoup
import re

class ArticlesSpider(scrapy.Spider):
    name = "articles"

    download_delay = 1

    start_urls = [
        'https://medium.com/topics'
    ]

    def parse(self, response):
        #fetches the pages for each medium topic
        links = response.css('a')
        for i in range(19, 204):
            soup = BeautifulSoup(links[i].extract(), 'html.parser')
            link = soup.a.get('href')
            yield response.follow(link, callback=self.parseTopics)


    def parseTopics(self, response):
        #fetches the 10 latest articles for each topic page
        sections = response.css('.o')
        for i in range(6, 34, 3):
            soup = BeautifulSoup(sections[i].extract(), 'html.parser')
            linkEnd = soup.a.get('href')
            fullLink = 'https://medium.com' + linkEnd
            yield response.follow(fullLink, callback=self.parseArticles)


    def parseArticles(self, response):
        #extract the text from each article and write it to file
        filename = "./sampleText.txt"
        with open(filename, 'a') as f:
            for paragraph in response.css('.graf--p').extract():
                soup = BeautifulSoup(paragraph, 'html.parser')
                text = soup.get_text()

                #post processing
                text = text.replace('( ', '(')
                text = text.replace('\u201c', '"')
                text = text.replace('\u201d', '"')
                parentheticals = re.findall('\([^()]*\)', text)
                quotes = re.findall('"[^"]*"', text)
                for paren in parentheticals:
                    words = paren.split(' ')
                    if len(words) > 3:
                        text = text.replace(paren, paren[1:len(paren) - 1])
                for quote in quotes:
                    words = quote.split(' ')
                    if len(words) > 3:
                        text = text.replace(quote, quote[1:len(quote) - 1])

                text = re.sub('Sources.*', '', text, flags=re.DOTALL)
                text = re.sub('References.*', '', text, flags=re.DOTALL)
                text = re.sub('Further Reading.*', '', text, flags=re.DOTALL)
                text = re.sub(' .*@.*', '', text, flags=re.DOTALL)
                text = re.sub('http.*', '', text)
                text = re.sub('www.*', '', text)
                text = re.sub('Credit:.*', '', text)
                text = re.sub('Copyright.*', '', text)
                text = re.sub('\u00A9.*', '', text)
                text = re.sub('\u00Ae.*', '', text)
                text = re.sub('Trademark.*', '', text)
                text = re.sub('Illustration:.*', '', text)
                text = re.sub('Illustrations:.*', '', text)
                text = re.sub('Photo:.*', '', text)
                text = re.sub('Photo by.*', '', text)
                text = re.sub('\[\d\]', '', text)
                text = re.sub('\(\d\)', '', text)
                text = re.sub('\d\)', '', text)
                text = re.sub('#\d', '', text)
                text = text.strip()
                text = re.sub(' +', ' ', text)

                f.writelines(text + '\n')
            f.close()
