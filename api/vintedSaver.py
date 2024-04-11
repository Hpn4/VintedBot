from api.vintedDataStruct import *
import csv
import os

class Saver:

    def __init__(self):
        self.saverPath = "api/cache/"
        self.colorPath = self.saverPath + "colors.csv"
        self.brandPath = self.saverPath + "brands.csv"

    def exists(self):
        return os.path.exists(self.colorPath) and os.path.exists(self.brandPath)

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