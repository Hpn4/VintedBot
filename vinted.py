import api.scrapper as vapi
from api.vintedSaver import *
import api.getbrand as ia
import api.getmost as iac
import os
import shlex

class color:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'

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
    saver.saveBrands(api.get_brands())
    saver.saveColors(api.get_colors())

def printCmd(name, descr):
    print(color.lightblue + name + color.reset + ":", descr)
def printHelp():
    printCmd("list locale", "List all your locals items in format (name, size, brand)")
    printCmd("list remote", "List all your items on your account in format (name, size, brand)")
    printCmd("brand list", "List detected brands")
    printCmd("brand add NAME", "Add the NAME brand")
    printCmd("brand remove NAME/ID", "Remove the brand with the given NAME or given ID")
    printCmd("color list", "List detected colors")
    printCmd("color add NAME HEX", "Add the NAME color with the given HEX value")
    printCmd("color remove NAME/ID", "Remove the color with the given NAME or given ID")
    printCmd("guess brand IMAGE", "Guess the brand (among detected brand) of the given cloth (you can put relative or absolute path)")
    printCmd("guess color IMAGE", "Guess the color (among detected color) of the given cloth (you can put relative or absolute path)")
    printCmd("exit", "quit the program")

def handleListCmd(args):
    if len(args) == 1:
        print("Invalid mode, must be: locale or remote")
        return

    if args[1] == "remote":
        formatter = displayTop(["NAME", "SIZE", "BRAND"], [0.6, 0.2, 0.2])
        for item in api.get_user_item(userid, 100000):
            displaySingle([item.title, item.size, item.brand], formatter)
        return

    if args[1] == "locale":
        print("TODO")
    else:
        print("Invalid mode, must be: locale or remote")

def printErr(s):
    print(color.red + s + color.reset)

def handleGuessCmd(args):
    if len(args) == 1:
        printErr("Invalid mode, must be: brand or color")
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
        labels = ia.getbrands([path])[0]
        displaySingle([labels["label"], str(labels["score"])], formatter)
    elif args[1] == "color":
        formatter = displayTop(["NAME", "VALUE"], [0.2, 0.4])
        hexv, name = iac.getcolor(path)
        displaySingle([name, str(hexv)], formatter)
    else:
        printErr("Invalid mode, must be: brand or color")


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

def tryPost(args):
    _, title, descr, price, photo = args
    price = int(price)

    api.post_item(ddk, title, descr, price, [photo])

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
    elif cmd == "guess":
        handleGuessCmd(args)
    elif cmd == "post":
        tryPost(args)
    else:
        printErr("Command not found.")
