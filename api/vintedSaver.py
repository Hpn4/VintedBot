from api.vintedDataStruct import *
import urllib.request
import csv
import os
import json

class Saver:

    def __init__(self):
        self.saverPath = "api/cache/"
        self.colorPath = self.saverPath + "colors.csv"
        self.brandPath = self.saverPath + "brands.csv"
        self.sizePath = self.saverPath + "size.csv"
        self.scrapped = "scrapped"

    def exists(self):
        return os.path.exists(self.colorPath) and os.path.exists(self.brandPath) and os.path.exists(self.sizePath)

    def saveSizes(self, sizes):
        with open(self.sizePath, 'w', newline='') as csvfile:
            fieldnames = ['id', 'title']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for size in sizes:
                writer.writerow({'id': size.id, 'title': size.title})

    def saveColors(self, colors):
        with open(self.colorPath, 'w', newline='') as csvfile:
            fieldnames = ['id', 'title', 'hex', 'order']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for color in colors:
                writer.writerow({'id': color.id, 'title': color.title, 'hex': color.hex, 'order': color.order})

    def saveBrands(self, brands):
        with open(self.brandPath, 'w', newline='') as csvfile:
            fieldnames = ['id', 'title']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for brand in brands:
                writer.writerow({'id': brand.id, 'title': brand.title})

    def saveItem(self, item, force):
        if not os.path.exists(self.scrapped):
            os.mkdir(self.scrapped)

        path = self.scrapped + "/" + str(item.id)
        if os.path.exists(path):
            if not force:
                return
        else:
            os.mkdir(path)

        with open(path + '/data.json', 'w', encoding='utf-8') as f:
            json.dump(item.__dict__, f, ensure_ascii=False, indent=4)

        for i in range(len(item.photos)):
            urllib.request.urlretrieve(item.photos[i], f"{path}/{i}.jpg")

    def loadSizes(self):
        sizes = []
        with open(self.sizePath, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                sizes.append(Size(row))

        return sizes

    def loadColors(self):
        colors = []
        with open(self.colorPath, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                colors.append(Color(row))

        return colors

    def loadBrands(self):
        brands = []
        with open(self.brandPath, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                brands.append(Brand(row))

        return brands

    def loadItem(self, itemId):
        path = self.scrapped + "/" + str(itemId) + "/data.json"
        if not os.path.exists(path):
            return None

        f = open(path, "r")
        item = Item(json.load(f))
        f.close()

        return item

    def loadItems(self):
        items = []

        for file in os.listdir(self.scrapped):
            items.append(self.loadItem(file))

        return items

    def deleteItem(self, itemId):
        path = self.scrapped + "/" + str(itemId)
        if not os.path.exists(path):
            return

        for file in os.listdir(path):
            os.remove(f"{path}/{file}")

        os.rmdir(path)

    def deleteItems(self):
        for file in os.listdir(self.scrapped):
            self.deleteItem(file)
