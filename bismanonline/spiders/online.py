import scrapy
import pandas as pd
df = pd.read_csv('F:\Web Scraping\Golabal\keywords.csv')
base_url = 'https://touch.bismanonline.com/content/action/Search?pager=1&doSearch=True&&scTab=&q={}&doSearch=True&sto=on&alm_st=&alm_sd=&app_p=1'

class OnlineSpider(scrapy.Spider):
    name = 'online'
    header = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
        'cache-control': 'no-cache' ,      
        'dnt': '1',
        'pragma': 'no-cache ',       
        'save-data':'on',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    def start_requests(self):
        for index in df:
            yield scrapy.Request(base_url.format(index), headers=self.header, cb_kwargs={'index':index})

    def parse(self, response, index):
        total_pages = response.xpath("//div[@class='ui card BMO35-listPagerContainer']/a[last()-1]/text()").get()
        # print(total_pages)
        current_page =response.css("a.BMO35-listPagerCurrent::text").get()
        # print(current_page)
        url = response.url
        header = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
            'cache-control': 'no-cache' ,      
            'dnt': '1',
            'pragma': 'no-cache ',       
            'save-data':'on',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
        }
        if total_pages and current_page:
            if int(current_page) ==1:
                for i in range(2, int(total_pages)+1): 
                    min = 'app_p='+str(i-1)
                    max = 'app_p='+str(i)
                    url = url.replace(min,max) 
                    # print(url)            
                    yield response.follow(url, cb_kwargs={'index':index})
        links = response.css(".bmoAdListRow_title_bigSinglePhoto a::attr(href)")  
        # print(links)    
        for link in links:
            yield response.follow("https://touch.bismanonline.com"+link.get(), callback=self.parse_item, cb_kwargs={'index':index})  
     
        
    def parse_item(self, response, index): 
        print(".................")  
        # print(response.url)           
        image_link = response.css('.bmoAVImgMain-a::attr(src)').get()
        # print(image_link)
        raws = response.xpath('//div[5]/div[2]/span[2]//text()').get().strip()
        raw = raws[:-15]
        auction_date = raw[-21:]
        # print(auction_date)          
        location = response.css(".adListRow_mobile_userLocation::text").get()
        # print(location)
        product_name = response.css(".bmoAV_title::text").get()
        # print(product_name)
        lot = response.css(".BMOAVSection1-adNumber-a span::text").get()
        lot_number = lot[4:]
        # print(lot_number) 
        description = response.css(".BMOAVSection1-descriptionBox-a::text").get()
        # print(description)   
        auctioner = response.css('.adListRow_mobile_userContainerScreenName a::text').get()
        # print(auctioner)    
        
        yield{            
            'product_url' : response.url,           
            'item_type' :index.strip(),            
            'image_link' : image_link,          
            'auction_date' : auction_date,            
            'location' : location,           
            'product_name' : product_name,            
            'lot_id' : lot_number,          
            'auctioner' : auctioner,
            'description' : description,
            'website' : "bismanonline"            
        }