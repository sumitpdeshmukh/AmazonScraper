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
        str = response.xpath('//span[@id="productTitle"]/text()').extract() # Working
        item['product_name'] = str[0].strip(' \t\n\r')
        str = response.xpath('//a[@id="brand"]/text()').extract()           # Working
        item['brand'] = str[0].strip(' \t\n\r')
        str = response.xpath('//span[@id="priceblock_ourprice"]/text()').extract() # Working
        item['price'] = (str[0].strip(' \t\n\r'))
        str = response.xpath('//span[@id="acrCustomerReviewText"]/text()').extract() # Working
        str = re.sub(r'[a-zA-Z]','',str[0]).strip(' \t\n\r')
        item['numreviews'] = str
        str = response.xpath('//div[@class="content"]/ul/li[1]/text()').extract()   
        str = re.sub(r'\(','',str[0]).strip(' \t\n\r')
        item['item_weight'] = str
        str = response.xpath('//div[@class="content"]/ul/li[2]/text()').extract()   
        str = re.sub(r'\W','',str[0]).strip(' \t\n\r')
        item['item_origin'] = str
        #----------------------------------------------------------------------------#
        str = response.xpath('//div[@class="content"]/ul/li[3]/text()').extract()   
        str = re.sub(r'\W','',str[0]).strip(' \t\n\r')
        item['item_ASIN'] = str
        #---------------------------------------------------------------------------#
        str = ""
        list_str = response.xpath('//div[@class="content"]/ul/li[5]/text()').extract()
        str = str.join(list_str).strip(' \t\n\r()')
        item['item_rank'] = str
        #---------------------------------------------------------------------------#
        str = ""
        list_str = response.xpath('//a[@class="a-link-normal a-color-tertiary"]/text()').extract()
        i = 0
        #item['amazon_category'] = str.join(list_str) # Try this with Lambda and join.
        for st in list_str:
            str += st.strip(' \t\n\r')
            i = i + 1
            if(len(list_str) != i):
                str += " > "           
        item['amazon_category'] = str

        #print(response.xpath('//a[@class="a-link-normal a-color-tertiary"]/text()').extract())
        #print(response.xpath('//span[@id="detail-bullets"]/text()').extract())
        yield item

        #for url in response.xpath('//a/@href').extract():
        #    yield scrapy.Request(url, callback=self.parse)
        
        #print(response.xpath('//span[@id="productTitle"]/text()').extract())