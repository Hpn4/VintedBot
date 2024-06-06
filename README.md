# Vinted Automation

This bot will call API endpoints of the French vinted website (`www.vinted.fr`)

If you want more fonctionalities you can open an issue.

This project is still in development

## Install

This bot use an AI to extract brand and color from cloth in images so the installation can be quiet long and take some place (~4Go).

I recommand to run the bot in a virtual env because there is a lot of dependencies.

The first run will download a model from HuggingFace and will setup some cache. Future run will be faster.

### On Linux

```bash
python -m venv my-env # Will create a virtual envrionment in the folder my-env
. my-env/bin/activate # Will activate the virtual environment
pip install -r requirement.txt # Download all the dependencies
python vinted.py
```

### On windows

Open a powershell and run

```bash
pip install virtualenv
virtualenv --python C:\Path\To\Python\python.exe my-env
.\my-env\Scripts\activate # Activate the virtual env
pip install -r requirement.txt # Download all the dependencies
python vinted.api
```

## Run setup

In order to use the vinted API, the Bot need three information that you need to put in the `cookies.txt` file:
- The userid that will effectuate all the actions. It can be found in the URL of the homepage of the user : `https://www.vinted.fr/member/ID`
- The vinted session id. It's a pretty huge cookie named `_vinted_fr_session` you can find it using the web inspector.
- Datadome session. In order to generate it, I recommand that you start publishing an article. Just put random value in the textfield and try to send the article. The goal here is not creating a real publication but to generate a viable datadome token (datadome use AI based on how user interact with the website: mouse clicks, mouse movements, key pressed...). Then you can find a cookie called `datadome`. 

All values must be put below the line starting with a `>`, for example a valid `cookies.txt` file will be:
```
> Put your userid below:
1234567890

> Put your vinted session id below:
A-very-long-session-id-cookie

> Put your datadome token below:
datadomecookie
```

The vinted_session_id and datadome cookies are short lived tokens. If you don't use the bot during more than an hour, you need to redo the steps.
Note that the datadome cookies is requiered only if you want to post an article.

## Commands

You can type `help` to list all the available commands and a small description. Here are some implemented use case:
- fetch items: will download all items or item with a specific ID from an account (the one in the cookie.txt file so it's not necessarily yours)
- list items: locally (saved from fetch) or remotly (account in the cookie.txt file)
- delete items: locally (saved from fetch) or remotely (work only if your are the owner)
- post items: all locally saved items (from fetch) or item with specific ID. The images will also be posted.

## Limitations

Not all data are saved for items, only:
- price
- title
- description
- brand
- colors
- size
- catalog id (what's the item)