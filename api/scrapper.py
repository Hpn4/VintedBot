from requests_toolbelt import MultipartEncoder
from api.vintedDataStruct import *
from api.color import color
import requests
import json
import os.path
import os
import time
import cloudscraper
import csv

#userid = "20309940"
#userid="173647952"

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

    def get_endpoint(self, endpoint):
        r = self.s.get(f"{self.baseUrl}/{endpoint}")

        if r.status_code == 401:
            print(color.red + "Your session id is not set or expired" + color.reset)
        elif r.status_code == 404:
            print(color.red + "Invalid ID" + color.reset)
        elif r.status_code != 200:
            print(r, r.text) 

        return r

    def get_user_item(self, userid, item_id):
        r = self.get_endpoint(f"items/{item_id}")

        if r.status_code == 200:
            js = r.json()
            return Item(js['item'])

    def get_user_items(self, userid, count):
        r = self.get_endpoint(f"users/{userid}/items?per_page={count}")
 
        items = []

        if r.status_code == 200:
            js = r.json()

            for item in js['items']:
                items.append(Item(item))

        return items

    def delete_item(self, itemid):
        url = f"{self.baseUrl}/items/{itemid}/delete"
        r = self.s.post(url)

        if r.status_code == 200:
            print(r.json())
        else:
            print(r, r.text)
            return False

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

    def get_sizes(self):
        req = self.s.get(f"{self.baseUrl}/size_groups")

        js = req.json()
        js = js["size_groups"][2]
        sizes = []
        for size in js['sizes']:
            sizes.append(Size(size))

        return sizes

    def post_datadome(self, ddk):
        self.s.headers['Referer'] = "https://www.vinted.fr/"
        self.s.headers['Content-Type'] = "application/x-www-form-urlencoded"
        req = self.s.post("https://dd.vinted.lt/js", data={"ddk": ddk})

        token = req.json()['cookie']
        token = token.split("datadome=")[1].split(";")[0]

        del self.s.headers['Referer']

        return token

    def post_item_intern(self, ddk, tempuuid, photo_ids, item):
        header = self.s.headers.copy()

        header['Referer'] = "https://www.vinted.fr/items/new"
        header['Content-Type'] = "application/json"
        header['X-Money-Object'] = "true"
        header['Cookie'] = f"datadome={ddk}; _vinted_fr_session={self.session_id};"

        photos = ""
        if len(photo_ids) > 0:
            photos = """{"id":%s,"orientation":0}""" % photo_ids[0]
            for i in range(1, len(photo_ids)):
                photos += """,{"id":%s,"orientation":0}""" % photo_ids[i]
        
        colors = ""
        if len(item.colors) > 0:
            colors = str(item.colors[0])
            for i in range(1, len(item.colors)):
                colors += "," + str(item.colors[i])

        # Actual post
        data = """{"item":{"id":null,"currency":"EUR",
        "temp_uuid":"%s",
        "title":"%s",
        "description":"%s",
        "brand":"%s",
        "size_id": %d,
        "catalog_id":%d,
        "isbn":null,"is_unisex":false,
        "status_id":2,
        "video_game_rating_id":null,
        "price":%d,
        "package_size_id":1,
        "shipment_prices":{"domestic":null,"international":null},
        "color_ids":[%s],
        "assigned_photos":[%s],
        "measurement_length":null,"measurement_width":null,"item_attributes":[{"code":"material","ids":[]}]},"feedback_id":null}
        """ % (tempuuid, item.title, item.description.replace('\n', "\\n"), 
            item.brand, item.size_id, item.catalog_id,
            float(item.original_price_numeric), colors, photos)

        # "color_ids":[1,2],
        # "brand_id":172724,
        # "size_id":209,

        # Swap headers
        prev = self.s.headers
        self.s.headers = header

        # Post datapost Test description 10 dataset/color/bleu.jpg
        req = self.s.post("https://www.vinted.fr/api/v2/items", json=json.loads(data))
        # Restore headers
        self.s.headers = prev

        if req.status_code != 200:
            print(r, r.text)
            return False

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

        # Build request
        m = MultipartEncoder(Q, boundary="----WebKitFormBoundaryQrHoB6QjnAG5GpjS")
        header['Content-Type'] = m.content_type

        r1 = requests.Request("POST", "https://www.vinted.fr/api/v2/photos", headers=header, data=m.to_string())

        session = requests.Session()
        prepped = session.prepare_request(r1)
        res = session.send(prepped, verify=False)

        if res.status_code != 200:
            print(res, res.text)
            return False

        return res.json()['id']

    def post_item(self, ddk, item):
        req = self.s.get("https://www.vinted.fr/items/new")

        t = req.text
        ddk1 = t.split('DATADOME_CLIENT_SIDE_KEY\\\":\\\"')[1].split("\\\"")[0]
        temp_uuid = t.split('tempUuid\\\":\\\"')[1].split("\\\"")[0]

        print("DDK =", ddk1)
        print("TEMP UUID =", temp_uuid)

        ddk1 = self.post_datadome(ddk1)

        photo_ids = [self.post_photos(ddk, photo, temp_uuid) for photo in item.photos]
        return self.post_item_intern(ddk, temp_uuid, photo_ids, item)

### URLS
# /api/v2/package_sizes HTTP/2 : shipping packet size
# /api/v2/statuses HTTP/2 : etat du produit
# /api/v2/colors HTTP/2 : couleurs possibles
# /api/v2/size_groups HTTP/2 : toutes les tailles possibles

# /api/v2/users/173647952/stats HTTP/2 : nombres de msg, push up...

# api/v2/users/173647952/items?page=1&per_page=20&order=relevance
# /relay/events : tell what action the user does (each click)