import scrapy
import re
from amazon.items import AmazonItem

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com"]
    start_urls = [
        "https://www.amazon.com/gp/product/B00XMVRVJM/ref=s9_simh_gw_g200_i2_r?ie=UTF8&fpl=fresh&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=&pf_rd_r=10TVW2TVJTX0D37XKQ78&pf_rd_t=36701&pf_rd_p=6aad23bd-3035-4a40-b691-0eefb1a18396&pf_rd_i=desktop"
    ]

    def parse(self, response):
        item = AmazonItem()
        str = response.xpath('//span[@id="productTitle"]/text()').extract()
        item['product_name'] = str[0].strip(' \t\n\r')
        str = response.xpath('//a[@id="brand"]/text()').extract()
        item['brand'] = str[0].strip(' \t\n\r')
        str = response.xpath('//span[@id="priceblock_ourprice"]/text()').extract()
        item['price'] = str[0].strip(' \t\n\r')
        str = response.xpath('//span[@id="acrCustomerReviewText"]/text()').extract()
        str = re.sub(r'[a-zA-Z]','',str[0]).strip(' \t\n\r')
        item['numreviews'] = str
        yield item
        #print(response.xpath('//span[@id="priceblock_ourprice"]/text()').extract())
        #print(response.xpath('//span[@id="productTitle"]/text()').extract())