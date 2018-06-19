import scrapy


class PhonesTabletsSpider(scrapy.Spider):
    name = "phones_tablets"

    def start_requests(self):
        with open('urls.csv') as f:
            urls = f.readlines()
        urls = [x.strip() for x in urls]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if 'https://www.daraz.lk/phones-tablets/?page=' in response.url:
            # listing page
            links = response.xpath('//section[@class="products"]/div[contains(@class, "sku -gallery")]/a/@href').extract()
            for link in links:
                yield scrapy.Request(link, callback=self.parse)
        else:
            # restaurant page
            title = response.xpath('//div[@class="details -validate-size"]/span/h1/text()').extract_first()
            by = response.xpath('//div[@class="sub-title"]/a/text()').extract_first()
            total_ratings = response.xpath('//div[@class="total-ratings"]/text()').extract_first()
            average_rating = response.xpath('//*[@id="ratingReviews"]/section[1]/article[2]/div/span').extract_first()
            brand = response.xpath('//div[@class="list -features -compact"]/ul/li[2]/text()').extract_first()
            model = response.xpath('//div[@class="list -features -compact"]/ul/li[3]/text()').extract_first()
            rom = response.xpath('//div[@class="list -features -compact"]/ul/li[4]/text()').extract_first()
            price = response.xpath('//div[@class="price-box"]/div/span/span[2]/text()').extract_first()

            another_seller = response.xpath('//*[@id="sellersPanel"]/div/div[2]/div[1]/a/text()').extract_first()
            another_seller_rating = response.xpath(
                '//*[@id="sellersPanel"]/div/div[2]/div[2]/div[1]/div/span/text()').extract_first()
            yield {
                'title': title,
                'by': by,
                'brand': brand,
                'model': model,
                'rom': rom,
                'price': price,
                'total_ratings': total_ratings,
                'average_rating': average_rating,
                'another_seller': another_seller,
                'another_seller_rating': another_seller_rating
            }
