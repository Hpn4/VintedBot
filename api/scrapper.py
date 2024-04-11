from requests_toolbelt import MultipartEncoder
from api.vintedDataStruct import *
import requests
import json
import os.path
import os
import time
import cloudscraper
import csv

#userid = "20309940"
#userid="173647952"
#session_id = "ZVJlU0JNZEhqWFUrcnl0VWNqRVYzcWhHM1lFWTRrdkx0VkpLL0xVL1NNOHhkZ0hadnY3dk1lWVpXZklZS0ZTNGxObmZCUm1Jd2lvckFBbHlyYUdiZW5DVWFVT3ZZcE5rVHd3SDZaMEE3TTlwS3A3OUVQbjhKdExkcnhaZ29IVDhXclRMS0JLWDJVblJobWZTUjU4SmlLU0JPOUZTODUyOVFxM0RTa05RMFJFdW1ML2g4S3NsK2MyS1pjb1lpdmRBWWZwMk4vNjA3bE9KVDl6T0FQOVpBUkJrdUdzTzZsYjdGT2dsaHlnelFKQzRRTGJJNXp1UGtMTnY0UjBsVDJ2L1plQVFpMUhEYkR1bEMxL2RoOWpweEZxNmZMdm1RMHVOKzFRQmdOQ3lqS2Y4TE8rdWFWcFJZUDFQM0FpV1JxRDJmM3BHNEVXenFFcjcwbFNxd09Rc21rS2tiR09lZmJvYks5TzVIb2J0NE1OYllFVjY1YnIvTThNQnRHczEwWjR1bjd6Ny8wT2VEWktaREFPMWZoNmQwKzBPakpnZ1ZIc2hsOEx4ZUtZd04xMzV0c3A4YTdRSnJuRG5xUmVKaldPcDQ1SzhBLyszUEgzTmJJTXQ1a1VBK3lhU0tpOWVuME9aMzB0OUhYQW1FcEhYZDVKSk5kZXBZbHJzemUvQXhKRHNsZ0w0eGZDMFpFdW5Zc0x1dVJTSVlQUk1rYUNsTnM4ekV0bTM0Q2RZdzBJUWtEYkEwYlJ2WTRWUWVkc0EzakI1R3poT0lFdWQrMU4vb3JZTHpJOE9xakU5UFVVWE50OE1DMXBJc3pCbjFTVmpFb0hXeGdIcnRFVjRma1ZaMm4rQ2xmakFWelZrWGVGREIrbHd3MERmbjRyVkxheUE3MVFMMUNNYzhsSnlTYkk1NjRIYkd2SWNHNFFHWjZIb2tKVUxQK01TaHpWd0VtaHAzYXgybjZsbW5KNTJqWGIyWFBZS2xZdll1Z2RwK0tJNGJ4c2EzMWlGYVNySjdoaUpJVHhsT1d4OWM1QiszN2JqK2lqZWk1b3phcVVlVkJ4K0czbHducmh5SEJXNkgyWTFhMVBnbWp3MlJjM2hyd1ovREw0SHJMVzJTb0MyWjFzVkYyLzlCeWpoN2drTlYzZU1ia3c0N2RtRzlJSE40VyszT01BY1NXdm5qT3ZyamNDWjdUTmJEbEVYTmZsMkozaDREd1Q4QmRzRWZFUzR1Z1NydGlLNTBoVndWY1lPcUwxbDJ5bTV5SlY2R3NDZitpQjVkMEdiVlV3QzJjUVE1RjZCMUdWaVlzTmF3MUpXdWdraVZlUzVNTDVYYjkwUlkycXZyWkJtTGNrRFNDRFlvKzRCVHk3MU03NFlIaTBGNW5kK0RCOFlrUlJrRldqdWYxU0IxWkk1c2NpcEdxQWljK2dLd29PVGdLRllUcTVhMDdobks4UUdFZmU5dDhaa1JkOGxudktBMlZaMVRGZ1kyQklZaDFoUnh5b0ZYVTI5eWlBZGNXamd3NG4xZzJLWCtnMWliWXBWaEZFTTRnTlZDWnhyZ1ByK09NNWRSVHZFVitPbGJYTkFYVTdsWW54V0JvZzROZ1MwNllIdlF4OTJuaitQdi9tNS9FV3hqaW5mVE9UYU1sZjgrUy92OFc3Zmt4UHRMcXhkU0lPUVV0RlNhaGFsK3pJcjgvSUFaRjdHYVhmOTNMRnpVVlJQait5STZScmRZNGpEb0xFbVJuNVdweCtGTnFSY0lSYXA0NC9aOENGSGhUSEUrWkl4ZlMxMjNHWDAzYk1HMXpCQVVieDNNWVVIdTJ5RkVMbnBvVEVBNEdnemVhMzlmckhFRUwvSjBkSHc1cVF6emNnSFdYWFpsQkJ2MnFXdTN1MWtHUEpjWFAxOEQxNnlndEhoc1czUlUyeStjWU1nWURlaGdMTW9OWFVWZktic0VOK0JiRDV3Q3pESkpYdWxGeUdZQUFNdzZLdXl3REhnUk1XUmdJTThuN1pTdDZJZUxQbjdKMEtsUnAxWHdMQUhhRW10WEFEVFVGaXlQSWhabnZtcXNUZVpoZTZtKzk4UVZMbXVQN1AvS1NRQzNUd3BpcGtDN1FXUlNLakRsYmY0emZCS3ZQT0xxRUdob2JKS2k2THZsQ0xwYlJ4b0ErNWgrR1NLd0JtRVNPVk53K1JQVGNKUHRKbklOY1FLb2ptZVhnalV3KzVtNDlXQ2trWVpaekdyTWQ0SkJMYWxzcXVoV2E3RG9zemlMSlF5SHJpRWpNaEd2T1pJcm85SjV1Y2wvdGczd0w4RTh5aWtIcWMrWkt1cE1EYlhJbWt1SFBkbVJtc25tZjlRMTFnZU5EaFhHczZDY29WS05HNVJhOU9ERHJQZ3lxdEpqcVp6VUhwQzdyZXI3ZU1rSXlkYUNrNStkQ3orUlhUVFJ4ajlnU2NwRU5Cdll2bHBUYktkYnA0UnhLYWhQdVpUcTlXVjkwZExvNC9KWmNuajJNb2pkdVd5UWVNSDNBPT0tLUVCcFlFNkNlRTdheW8zcGlTa2RqTnc9PQ%3D%3D--c3a1964e6596a1b90db45a2e667cadf4068b0709"

class VintedAPI:

    def __init__(self, session_id, userid):
        self.s = cloudscraper.create_scraper()
        self.s.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'fr',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'TE': 'Trailers',
            'Cookie': f"_vinted_fr_session={session_id};"
        }

        # Get CSRF token
        res = self.s.get("https://www.vinted.fr/").text
        csrfToken = res.split('CSRF_TOKEN\\":\\"')[1].split('\\"')[0]

        self.s.headers['X-Csrf-Token'] = csrfToken
        self.csrf = csrfToken

        self.userid = userid
        self.session_id = session_id
        self.baseUrl = "https://www.vinted.fr/api/v2"

    def get_user_item(self, userid, count):
        url = f"{self.baseUrl}/users/{userid}/items?per_page={count}"
        r = self.s.get(url)
    
        items = []

        if r.status_code == 200:
            js = r.json()

            for item in js['items']:
                items.append(Item(item))

        return items

    def delete_item(self, itemid):
        url = f"{self.baseUrl}/items/{itemid}/delete"
        r = self.s.post(url)

        print(r.status_code)
        if r.status_code == 200:
            print(r.json())

    def get_brands(self):
        req = self.s.get(f"{self.baseUrl}/brands")

        brands = []
        for brand in req.json()['brands']:
            brands.append(Brand(brand))

        return brands

    # Return array of all possible status (Very good state with etiquette, good state...)
    def get_statuses(self):
        req = self.s.get(f"{self.baseUrl}/statuses")

        statuses = []
        for status in req.json()['statuses']:
            statuses.append(Status(status))

        return statuses

    # Return an array of all possibles colors handled by vinted
    def get_colors(self):
        req = self.s.get(f"{self.baseUrl}/colors")

        colors = []
        for color in req.json()['colors']:
            colors.append(Color(color))

        return colors

    def post_datadome(self, ddk):
        self.s.headers['Referer'] = "https://www.vinted.fr/"
        self.s.headers['Content-Type'] = "application/x-www-form-urlencoded"
        req = self.s.post("https://dd.vinted.lt/js", data={"ddk": ddk})

        print(req.text)
        token = req.json()['cookie']
        token = token.split("datadome=")[1].split(";")[0]
        print(token)

        del self.s.headers['Referer']

        return token

    def post_item_intern(self, ddk, tempuuid, title, description, price, photo_ids):
        header = self.s.headers.copy()

        header['Referer'] = "https://www.vinted.fr/items/new"
        header['Content-Type'] = "application/json"
        header['X-Money-Object'] = "true"
        header['Cookie'] = f"datadome={ddk}; _vinted_fr_session={self.session_id};"

        photos = ""
        if len(photo_ids) > 0:
            photos = """{"id":%s,"orientation":0}""" % photo_ids[0]
            for i in range(len(photo_ids)):
                photos += """,{"id":%s,"orientation":0}""" % photo_ids[i]

        # Actual post
        data = """{"item":{"id":null,"currency":"EUR",
        "temp_uuid":"%s",
        "title":"%s",
        "description":"%s",
        "brand_id":172724,
        "brand":"Shein",
        "size_id":209,
        "catalog_id":1811,
        "isbn":null,"is_unisex":false,
        "status_id":6,
        "video_game_rating_id":null,
        "price":%d,
        "package_size_id":1,
        "shipment_prices":{"domestic":null,"international":null},
        "color_ids":[1,2],
        "assigned_photos":[%s],
        "measurement_length":null,"measurement_width":null,"item_attributes":[{"code":"material","ids":[]}]},"feedback_id":null}
        """ % (tempuuid, title, description, price, photos)

        # Swap headers
        prev = self.s.headers
        self.s.headers = header

        # Post datapost Test description 10 dataset/color/bleu.jpg
        req = self.s.post("https://www.vinted.fr/api/v2/items", json=json.loads(data))

        print(req.text)

        # Restore headers
        self.s.headers = prev

    def post_photos(self, ddk, file, tempuuid):
        header = self.s.headers.copy()

        header['Cookie'] = f"datadome={ddk}; _vinted_fr_session={self.session_id};"
        del header['Connection']
        del header['DNT']
        del header['TE']

        Q = {
        "photo[type]": (None, "item"),
        "photo[file]": (file, open(file, "rb"), "image/jpeg"),
        "photo[temp_uuid]": (None, tempuuid)
        }

        print(Q["photo[file]"])

        # Build request
        m = MultipartEncoder(Q, boundary="----WebKitFormBoundaryQrHoB6QjnAG5GpjS")
        header['Content-Type'] = m.content_type

        r1 = requests.Request("POST", "https://www.vinted.fr/api/v2/photos", headers=header, data=m.to_string())

        session = requests.Session()
        prepped = session.prepare_request(r1)
        res = session.send(prepped, verify=False)

        print(res, res.text)

        return res.json()['id']

    def post_item(self, ddk, title, description, price, photos):
        req = self.s.get("https://www.vinted.fr/items/new")

        t = req.text
        ddk1 = t.split('DATADOME_CLIENT_SIDE_KEY\\\":\\\"')[1].split("\\\"")[0]
        temp_uuid = t.split('tempUuid\\\":\\\"')[1].split("\\\"")[0]

        print("DDK =", ddk1)
        print("TEMP UUID =", temp_uuid)

        ddk1 = self.post_datadome(ddk1)

        photo_ids = [self.post_photos(ddk, photo, temp_uuid) for photo in photos]
        self.post_item_intern(ddk, temp_uuid, title, description, price, photo_ids)

#api = VintedAPI(session_id, userid)

#api.save_colors(api.get_colors())

# api.post_item("Salut je suis un gros test", "Si ça marche je suis refait", -42)
#for brand in api.get_brands():
#    brand.print()

#for items in api.get_user_item(userid, 6):
#    print(items.brand)

#api.post_photos("vide", "img.jpg", "tempuuid")
"""
items = api.get_user_item(userid, 20)
for item in items:
    api.delete_item(item.id)
"""
### URLS
# /api/v2/package_sizes HTTP/2 : shipping packet size
# /api/v2/statuses HTTP/2 : etat du produit
# /api/v2/colors HTTP/2 : couleurs possibles
# /api/v2/size_groups HTTP/2 : toutes les tailles possibles

# /api/v2/users/173647952/stats HTTP/2 : nombres de msg, push up...

# api/v2/users/173647952/items?page=1&per_page=20&order=relevance
# /relay/events : tell what action the user does (each click)