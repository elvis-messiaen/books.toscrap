import scrapy


class BooksSpiderSpider(scrapy.Spider):
    name = "books_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/category/books_1/index.html"]

    def parse(self, response):
        products = response.css("article.product_pod")

        for product in products:
            yield {
                'image_url': response.urljoin(product.css("div.image_container a img::attr(src)").get()),
                'url': response.urljoin(product.css("h3 a::attr(href)").get()),
                'star_rating': product.css("p.star-rating").attrib["class"].split()[-1],
                "title": product.css("h3 a::attr(title)").get(),
                "price": product.css("p.price_color::text").get(),
            }

