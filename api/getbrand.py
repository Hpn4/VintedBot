# Use a pipeline as a high-level helper
from transformers import pipeline
from api.vintedSaver import *
import sys
from transformers.utils import logging

logging.set_verbosity_error()

def getBrandsLabels():
    saver = Saver()
    return [x.title for x in saver.loadBrands()]

def getSizesLabels():
    saver = Saver()
    return [x.title for x in saver.loadSizes()][:-1]

def getBrands(images):
    pipe = pipeline("zero-shot-image-classification", model="openai/clip-vit-large-patch14")
    return [pipe(image, candidate_labels=getBrandsLabels())[0] for image in images]

def getSizes(images):
    pipe = pipeline("zero-shot-image-classification", model="openai/clip-vit-large-patch14")
    return [pipe(image, candidate_labels=getSizesLabels())[0] for image in images]