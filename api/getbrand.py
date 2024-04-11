# Use a pipeline as a high-level helper
from transformers import pipeline
from api.vintedSaver import *
import sys
from transformers.utils import logging

logging.set_verbosity_error()

def getlabels():
    saver = Saver()
    labels = ["Champion", "Adidas", "NFL", "Nike", "Reebok", "NHL", "Hunder Armour"]
    # labels = ["Red", "Blue", "Black", "Orange", "White", "Corail", "Gray", "Yellow", "Cyan", "Violet"]
    # labels = ["XS", "S", "M", "L", "XL"]

    # return [e + " cloth brand" for e in labels]
    labels = []
    for x in saver.loadBrands():
        labels.append(x.title)
    return labels

# model="rONIVALDO/brand-detector"
# pipe = pipeline("image-classification", model="barten/vit-base-patch16-224-brand")

def getbrands(images):
    pipe = pipeline("zero-shot-image-classification", model="openai/clip-vit-large-patch14")
    return [pipe(image, candidate_labels=getlabels())[0] for image in images]
