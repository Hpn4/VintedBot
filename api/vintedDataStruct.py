
class Status:
    def __init__(self, status):
        self.id = status['id']
        self.title = status['title']

    def print(self):
        print("---------- Status ----------")
        print("ID:", self.id)
        print("Title:", self.title)

class Item:
    def __init__(self, item):
        self.id = item['id']

        self.title = item['title']
        self.description = item['description']
        self.size = item['size'];
        self.brand = item['brand']
        # print(item['brand_id'])

        self.currency = item['currency']
        self.price = item['original_price_numeric']

        self.url = item['url']

        self.photos = []
        for img in item['photos']:
            self.photos.append(img['url'])

    def print(self):
        print("---------- Item ----------")
        print("ID:", self.id)
        print("Title:", self.title)
        print("Description:", self.description)
        print("Size:", self.size)
        print("Brand:", self.brand)
        print("Price:", self.price, self.currency)

        for photo in self.photos:
            print("Photos:", photo)

        print(self.url)

class Brand:
    def __init__(self, brand):
        self.id = brand['id']
        self.title = brand['title']

    def print(self):
        print("---------- Brand ----------")
        print("ID:", self.id)
        print("Title:", self.title)  

class Color:
    def __init__(self, color):
        self.id = color['id']
        self.title = color['title']
        self.hex = color['hex']
        self.order = color['order']

    def print(self):
        print("---------- Color ----------")
        print("ID:", self.id)
        print("Title:", self.title)
        print("Hex color:", self.hex)
        print("Order:", self.order)