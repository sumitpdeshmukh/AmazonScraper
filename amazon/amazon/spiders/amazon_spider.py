import scrapy
import re
from amazon.items import AmazonItem
from scrapy.selector import HtmlXPathSelector 
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AmazonSpider(CrawlSpider):
    name = "amazon"
    allowed_domains = ["amazon.com"]
    start_urls = [
        "https://www.amazon.com/gp/product/B00XMVRVJM/ref=s9_simh_gw_g200_i2_r?ie=UTF8&fpl=fresh&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=&pf_rd_r=10TVW2TVJTX0D37XKQ78&pf_rd_t=36701&pf_rd_p=6aad23bd-3035-4a40-b691-0eefb1a18396&pf_rd_i=desktop"
    ]
    start_url_category = "Sports & Outdoors > Sports & Fitness > Hunting & Fishing > Tactical & Personal Defense > Tactical Knives"
    already_crawled = []
    
    rules = (
        Rule(LxmlLinkExtractor(allow=(r'/dp',),deny=(r'/Detail/')), callback="parse_item", follow= True),
    )
#start_urls = [
	#"https://www.amazon.com/Mtech-Ballistic-Assisted-Tactical-Flipper/dp/B00RBF8EIC/ref=pd_sim_200_1?ie=UTF8&dpID=61mHW6oADBL&dpSrc=sims&preST=_AC_UL160_SR160%2C160_&psc=1&refRID=WFN5PJXS9PVQ836CX47G"
	#]
    
    def parse_item(self, response):
        item = AmazonItem()
        str = ""
        list_str = response.xpath('//a[@class="a-link-normal a-color-tertiary"]/text()').extract()
        i = 0
        item['amazon_category'] = str.join(list_str) # Try this with Lambda and join.
        for st in list_str:
            str += st.strip(' \t\n\r')
            i = i + 1
            if(len(list_str) != i):
                str += " > "
        if str != AmazonSpider.start_url_category: 
            return
        item['amazon_category'] = str
        str = response.xpath('//span[@id="productTitle"]/text()').extract() # Working
        item['product_name'] = str[0].strip(' \t\n\r')
        str = response.xpath('//a[@id="brand"]/text()').extract()           # Working
        item['brand'] = str[0].strip(' \t\n\r')
        str = response.xpath('//span[@id="priceblock_ourprice"]/text()').extract() # Working
        item['price'] = (str[0].strip(' \t\n\r'))
        str = response.xpath('//span[@id="acrCustomerReviewText"]/text()').extract() # Working
        str = re.sub(r'[a-zA-Z]','',str[0]).strip(' \t\n\r')
        item['numreviews'] = str
		#---------------------------------------------------------------------------#
        res = HtmlXPathSelector(response)
        contents = res.select('//div[@class="content"]/ul')
        for cont in contents.select('.//li'):			
            str = cont.select('.//b/text()').extract_first()
            if str == 'Shipping Weight:':
                val = cont.select('text()').extract()
                val = re.sub(r'\(','',val[0]).strip(' \t\n\r')
                item['item_weight'] = val
            if str == 'Origin:':
                val = cont.select('text()').extract()
                val = re.sub(r'\W','',val[0]).strip(' \t\n\r')
                item['item_origin'] = val
            if str == 'Amazon Best Sellers Rank:':
                val = ""
                list_str = cont.select('text()').extract()
                val = val.join(list_str).strip(' \t\n\r()')
                item['item_rank'] = val
            if str == 'ASIN: ':
                val = cont.select('text()').extract()
                val = re.sub(r'\W','',val[0]).strip(' \t\n\r')
                item['item_ASIN'] = val
            if str == 'Product Dimensions:':
                val = cont.select('text()').extract()
                val = re.sub(r'\W','',val[0]).strip(' \t\n\r')
                item['product_dim'] = val
        #----------------------------------------------------------------------------#
        str = ""
        contents = ""
        cont = ""
        contents = res.select('//table[@id="productDetails_detailBullets_sections1"]')
        for cont in contents.select('.//tr'):
            str = cont.select('.//th/text()').extract_first().strip()
            if str == 'Shipping Weight':
                val = cont.select('.//td/text()').extract()
                val = re.sub(r'\(','',val[0]).strip(' \t\n\r')
                item['item_weight'] = val
            if str == 'ASIN':
                val = cont.select('.//td/text()').extract()
                val = re.sub(r'\W','',val[0]).strip(' \t\n\r')
                item['item_ASIN'] = val
            if str == 'Best Sellers Rank':
                val = ""
                list_str = cont.select('.//td/span/span/text()').extract_first()
                val = val.join(list_str).strip(' \t\n\r()')
                item['item_rank'] = val
            if str == 'Item model number':
                val = cont.select('.//td/text()').extract()
                val = re.sub(r'\W','',val[0]).strip(' \t\n\r')
                item['model_num'] = val
            if str == 'Product Dimensions':
                val = cont.select('.//td/text()').extract()
                val = re.sub(r'\W','',val[0]).strip(' \t\n\r')
                item['product_dim'] = val
        #str = response.xpath('//div[@class="content"]/ul/li[1]/text()').extract()   
        #str = re.sub(r'\(','',str[0]).strip(' \t\n\r')
        #item['item_weight'] = str
        #str = response.xpath('//div[@class="content"]/ul/li[2]/text()').extract()   
        #str = re.sub(r'\W','',str[0]).strip(' \t\n\r')
        #item['item_origin'] = str
        #----------------------------------------------------------------------------#
        #str = response.xpath('//div[@class="content"]/ul/li[3]/text()').extract()   
        #str = re.sub(r'\W','',str[0]).strip(' \t\n\r')
        #item['item_ASIN'] = str
        #---------------------------------------------------------------------------#
        #str = ""
        #list_str = response.xpath('//div[@class="content"]/ul/li[5]/text()').extract()
        #str = str.join(list_str).strip(' \t\n\r()')
        #item['item_rank'] = str
        #---------------------------------------------------------------------------#
        str = ""
        
        #--------------------------------------------------------------------------------#
        str = response.xpath('//*[@id="reviewStarsLinkedCustomerReviews"]/i/span/text()').extract() #Not working
        str = str[0].strip(' \t\n\r')
        item['review_stars'] = str
        str = res.select('//*[@id="productDetails_detailBullets_sections1"]')
        item["product_url"] = response.request.url
		#print(response.xpath('//a[@class="a-link-normal a-color-tertiary"]/text()').extract())
        #print(response.xpath('//span[@id="detail-bullets"]/text()').extract())
        yield item

        #for url in response.xpath('//a/@href').extract():
        #    yield scrapy.Request(url, callback=self.parse)
        
        #print(response.xpath('//span[@id="productTitle"]/text()').extract())