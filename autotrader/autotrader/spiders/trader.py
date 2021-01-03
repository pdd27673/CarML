import scrapy
import json

class TraderSpider(scrapy.Spider):
    name = 'trader'
    allowed_domains = ['autotrader.com']

    custom_settings = {
        'FEED_URI': 'trader.json',
        'FEED_FORMAT': 'json'
    }

    def start_requests(self):
        url = 'https://www.autotrader.com/cars-for-sale/all-cars/cars-under-30000/moorpark-ca-93021?channel=ATC&relevanceConfig=default&dma=&searchRadius=100&isNewSearch=true&marketExtension=include&showAccelerateBanner=false&sortBy=relevance&numRecords=25'
        yield scrapy.Request(url)

    def parse(self, response):
        selected=response.xpath('.//script[contains(.,"BONNET_DATA__")]/text()').get()
        myselected=selected[23:]
        mydict=json.loads(myselected)
        myrealdict=mydict.get('initialState')
        mycars=myrealdict.get('inventory')

       for key in mycars:
            owner=mycars[key].setdefault('ownerName','')
            if owner!='Private Seller':
                continue

            try:
                id=mycars[key]['id']
                brand=mycars[key]['make']
                model=mycars[key]['model']
                notes=mycars[key].setdefault('trim','')
                price=mycars[key]['pricingDetail']['salePrice']
                km=mycars[key]['specifications']['mileage']['value']
                proDate=mycars[key]['year']
                url=mycars[key]['website']
            except:
                continue
            yield {
                'id':id,
                'brand':brand,
                'model':model,
                'notes':notes,
                'price':price,
                'km':km,
                'proDate':proDate,
                'url':url,
                'adDate':datetime.strftime(datetime.today(),'%Y-%m-%d')
            }
