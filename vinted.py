import api.scrapper as vapi
from api.vintedSaver import *
from api.color import color
from tqdm import tqdm
import api.getbrand as ia
import api.getmost as iac
import os
import shlex

cols = os.get_terminal_size()[0]

# Load tokens from the file
tokens = []
with open('cookies.txt', 'r') as file:
    for line in file.readlines():
        line = line.strip()
        if line.startswith(">") or line == "":
            continue

        tokens.append(line)

userid, session, ddk = tokens

# Load API
api = vapi.VintedAPI(session, userid)
saver = Saver()

def paddSpace(s, size):
    if len(s) > size:
        return s[0:size - 3] + "..."
    return s + " " * (size - len(s))

def displayTop(titles, size):
    formatter = [int(cols * i) for i in size]
    formatter[-1] = max(formatter[-1] - 3, 0)

    # Display title
    print(color.lightblue + paddSpace(titles[0], formatter[0]), end="")
    for i in range(1, len(titles)):
        print(" " + paddSpace(titles[i], formatter[i]), end="")
    print(color.reset)

    # Separation
    print(color.darkgrey + '-' * sum(formatter) + color.reset)

    return formatter

def displaySingle(row, formatter):
    print(paddSpace(row[0], formatter[0]), end="")
    for i in range(1, len(row)):
        print(" " + paddSpace(row[i], formatter[i]), end="")
    print()


# Download color and brand if they don't exist
def initCache():
    if saver.exists():
        print(color.green + "Cache already setup" + color.reset)
        return

    print(color.yellow + "Setup cache" + color.reset)
    os.mkdir(saver.saverPath)
    saver.saveBrands(api.get_brands())
    saver.saveColors(api.get_colors())
    saver.saveSizes(api.get_sizes())

def printCmd(name, descr):
    print(color.lightblue + name + color.reset + ":", descr)

def printHelp():
    print("="*10, "Item management", "="*10)
    printCmd("list local", "List all your locals items in format (name, size, brand)")
    printCmd("list remote", "List all your items on your account in format (name, size, brand)")
    printCmd("delete local all", "Delete all folders of saved items")
    printCmd("delete local ID", "Delete the folder of the item ID")
    printCmd("fetch all", "Download all your items and images on your account and save them in the scrapped directory (override items previsously storerd with the same id)")
    printCmd("fetch ID", "Download the item with id ID and his images and save it in the scrapped directory (override item previsously storerd with the same id)")
    printCmd("post all", "Upload all your local items and images on your account")
    printCmd("post ID", "Upload the local item with id ID and his images to your account")
    printCmd("boost ID", "Boost the item ID (by duplicating it and deleting ancient version)")
    printCmd("boost all", "Boost all your items (by duplicating them and deleting ancient version)")
    print("="*10, "Miscellaneous", "="*10)
    printCmd("brand list", "List detected brands")
    printCmd("brand add NAME", "Add the NAME brand")
    printCmd("brand remove NAME/ID", "Remove the brand with the given NAME or given ID")
    printCmd("color list", "List detected colors")
    printCmd("color add NAME HEX", "Add the NAME color with the given HEX value")
    printCmd("color remove NAME/ID", "Remove the color with the given NAME or given ID")
    printCmd("size list", "List all clothes size")
    print("="*10, "AI", "="*10)
    printCmd("guess brand IMAGE", "Guess the brand (among detected brand) of the given cloth (you can put relative or absolute path)")
    printCmd("guess color IMAGE", "Guess the color (among detected color) of the given cloth (you can put relative or absolute path)")
    printCmd("guess size IMAGE", "Guess the size (among detected sizes) of the given cloth (you can put relative or absolute path)")
    printCmd("exit", "quit the program")

def printErr(s):
    print(color.red + s + color.reset)

def handleListCmd(args):
    if len(args) == 1 or (args[1] not in ["remote", "local"]):
        print("Invalid mode, must be: local or remote")
        return

    items = []
    if args[1] == "remote":
        items = api.get_user_items(userid, 100000)
    else:
        items = saver.loadItems()

    formatter = displayTop(["ID", "NAME", "SIZE", "BRAND"], [0.1, 0.6, 0.1, 0.2])
    for item in items:
        displaySingle([str(item.id), item.title, item.size, item.brand], formatter)

def handleGuessCmd(args):
    if len(args) == 1:
        printErr("Invalid mode, must be: brand, size or color")
        return

    if len(args) != 3:
        printErr("Invalid syntax, type help")
        return

    path = args[2]

    if not os.path.exists(path):
        printErr("File not found")
        return

    if args[1] == "brand":
        formatter = displayTop(["BRAND", "POURCENTAGE"], [0.2, 0.2])
        labels = ia.getBrands([path])[0]
        displaySingle([labels["label"], str(labels["score"])], formatter)
    elif args[1] == "color":
        formatter = displayTop(["NAME", "VALUE"], [0.2, 0.4])
        hexv, name = iac.getcolor(path)
        displaySingle([name, str(hexv)], formatter)
    elif args[1] == "size":
        formatter = displayTop(["BRAND", "POURCENTAGE"], [0.2, 0.2])
        labels = ia.getSizes([path])[0]
        displaySingle([labels["label"], str(labels["score"])], formatter)
    else:
        printErr("Invalid mode, must be: brand, size or color")


def handleBrandCmd(args):
    if len(args) == 1:
        printErr("Invalid mode, must be: list, add or remove")
        return

    brands = saver.loadBrands()

    if args[1] == "list":
        formatter = displayTop(["ID", "NAME"], [0.2, 0.4])
        for brand in brands:
            displaySingle([brand.id, brand.title], formatter)
        return

    if args[1] == "remove":
        if len(args) != 3:
            printErr("Specify a name or an ID")
            return
        i = -1

        if args[2].isdigit():
            bid = int(args[2])
            for j in range(len(brands)):
                if bid == brands[j].id:
                    i = j
                    break
        else:
            for j in range(len(brands)):
                if args[2] == brands[j].title:
                    i = j
                    break

        if i != -1:
            del brands[i]

        saver.saveBrands(brands)
    elif args[1] == "add":
        if len(args) != 3:
            printErr("Specify a name")
            return

        for i in range(len(brands)):
            if args[2] == brands[i].title:
                return

        b = {"id": -1, "title": args[2]}
        brands.append(Brand(b))
        saver.saveBrands(brands)
    else:
        printErr("Invalid mode, must be: list, add or remove")

def handleSizeCmd(args):
    if len(args) == 1:
        printErr("Invalid mode, must be: list")
        return

    if args[1] == "list":
        formatter = displayTop(["ID", "NAME"], [0.2, 0.4])
        for size in saver.loadSizes():
            displaySingle([str(size.id), size.title], formatter)
        return
    else:
        printErr("Invalid mode, must be: list")


def handleColorCmd(args):
    if len(args) == 1:
        printErr("Invalid mode, must be: list, add or remove")
        return

    colors = saver.loadColors()

    if args[1] == "list":
        formatter = displayTop(["ID", "NAME", "HEX"], [0.1, 0.2, 0.2])
        for color in colors:
            displaySingle([color.id, color.title, color.hex], formatter)
        return

    if args[1] == "remove":
        if len(args) != 3:
            printErr("Specify a name or an ID")
            return
        i = -1

        if args[2].isdigit():
            bid = int(args[2])
            for j in range(len(colors)):
                if bid == colors[j].id:
                    i = j
                    break
        else:
            for j in range(len(colors)):
                if args[2] == colors[j].title:
                    i = j
                    break

        if i != -1:
            del colors[i]

        saver.saveColors(colors)
    elif args[1] == "add":
        if len(args) != 4:
            printErr("Invalid syntax, type help")
            return

        for i in range(len(colors)):
            if args[2] == colors[i].title:
                return

        b = {"id": -1, "title": args[2], "hex": args[3], "order": -1}
        colors.append(Color(b))
        saver.saveColors(colors)
    else:
        printErr("Invalid mode, must be: list, add or remove")

def handleFetchCmd(args):
    if len(args) == 1:
        printErr("Invalid mode, must be an ID or all")
        return

    items = []
    if args[1] == "all":
        items = api.get_user_items(userid, 100000)
    else:
        try:
            item_id = int(args[1])
            items = [api.get_user_item(userid, item_id)]
        except ValueError as verr:
            printErr("Invalid mode, must be an ID or all")
            return

    for i in tqdm(range(len(items)), desc="Fetching...", ascii=False, ncols=cols):
        saver.saveItem(items[i], True)


def handleDeleteCmd(args):
    if len(args) <= 2 or args[1] not in ["local", "remote"]:
        printErr("Invalid mode, must be: delete local/remote [ID]/all")
        return

    if args[1] == "local":
        if args[2] == "all":
            saver.deleteItems()
            return
        
        try:
            item_id = int(args[2])
            saver.deleteItem(item_id)
        except ValueError as verr:
            printErr("Invalid mode, must be an ID or all")
        return

    if args[2] == "all":
        items = api.get_user_items(userid, 100000)
        for i in tqdm(range(len(items)), desc="Deleting...", ascii=False, ncols=cols):
            api.delete_item(items[i].id)
        return
    
    try:
        item_id = int(args[2])
        api.delete_item(item_id)
    except ValueError as verr:
        printErr("Invalid mode, must be an ID or all")


def handlePostCmd(args):
    if len(args) == 1:
        printErr("Invalid mode, must be an ID or all")
        return

    if args[1] == "all":
        items = saver.loadItems()
        for i in tqdm (range(len(items)), desc="Fetching...", ascii=False, ncols=cols):
            api.post_item(ddk, items[i])
        return

    try:
        item_id = int(args[1])
        api.post_item(ddk, saver.loadItem(item_id))
    except ValueError as verr:
        printErr("Invalid mode, must be an ID or all")

def handleBoostCmd(args):
    if len(args) == 1:
        printErr("Invalid mode, must be an ID or all")
        return

    items = []
    if args[1] == "all":
        items = api.get_user_items(userid, 100000)
        items = [item.id for item in items]
    else:
        try:
            item_id = int(args[1])
            items = [item_id]
        except ValueError as verr:
            printErr("Invalid mode, must be an ID or all")
            return

    for i in tqdm (range(len(items)), desc="Boosting...", ascii=False, ncols=cols):
        item = api.get_user_item(userid, items[i])
        saver.saveItem(item, True)
        api.delete_item(items[i])
        api.post_item(ddk, saver.loadItem(items[i]))

initCache()
while True:
    args = shlex.split(input(color.cyan + "vinted > " + color.reset).strip())
    if len(args) == 0:
        continue

    cmd = args[0]

    if cmd == "exit":
        break
    elif cmd == "help":
        printHelp()
    elif cmd == "list":
        handleListCmd(args)
    elif cmd == "brand":
        handleBrandCmd(args)
    elif cmd == "color":
        handleColorCmd(args)
    elif cmd == "size":
        handleSizeCmd(args)
    elif cmd == "guess":
        handleGuessCmd(args)
    elif cmd == "fetch":
        handleFetchCmd(args)
    elif cmd == "delete":
        handleDeleteCmd(args)
    elif cmd == "post":
        handlePostCmd(args)
    elif cmd == "boost":
        handleBoostCmd(args)
    else:
        printErr("Command not found.")
