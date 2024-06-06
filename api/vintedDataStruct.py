
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
        self.size = item['size']
        self.size_id = item['size_id']
        self.brand = item['brand']
        self.catalog_id = item['catalog_id']
        self.package_size_id = item['package_size_id']
        self.status_id = item['status_id']
        self.colors = []
        if "colors" in item:
            self.colors = item['colors']
        for i in range(20):
            key = f"color{i}_id"
            if key in item:
                self.colors.append(item[key])

        self.currency = item['currency']
        self.original_price_numeric = item['original_price_numeric']

        self.url = item['url']

        self.photos = []
        i = 0
        for img in item['photos']:
            if type(img) == str:
                self.photos.append(f"scrapped/{self.id}/{i}.jpg")
                i += 1
            else:
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

class Size:
    def __init__(self, size):
        self.id = size['id']
        self.title = size['title']

    def print(self):
        print("---------- Size ----------")
        print("ID:", self.id)
        print("Title:", self.title)
