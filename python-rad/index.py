from PIL import Image, ImageDraw
import glob
import os
from super_image import EdsrModel, ImageLoader
import requests


def add_corners(im, rad):
    
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


files = []
for file in glob.glob(".\img\*.*"):
    files.append(file)
    

nb = 0;
strformat = ".png";

RADIUS = 50          # HERE FOR THE RADIUS-----------------------------------------------------------
RESOLUTION = 400     # CHANGE HERE FOR THE RESOLUTION --------------------------------------------------------------

for i in files:
    cut = i.split("\\")
    taillecut = len(cut)
    name = cut[taillecut-1]

    image = Image.open(i)
    new_image = image.resize((RESOLUTION, RESOLUTION))      
    new_image.save('.\imgdone\cut.png')
    im = Image.open('.\imgdone\cut.png')
    im = add_corners(im, RADIUS)               

    strnb = str(nb)
    strcomplete = '.\\imgdone\\'  + name + strformat
    im.save(strcomplete)

    image = Image.open(strcomplete)
    model = EdsrModel.from_pretrained('eugenesiow/edsr-base', scale=2)
    inputs = ImageLoader.load_image(image)
    preds = model(inputs)
    ImageLoader.save_image(preds, strcomplete)

    image = Image.open(i)
    new_image = image.resize((RESOLUTION, RESOLUTION))
    new_image.save(strcomplete)
    im = Image.open(strcomplete)
    im = add_corners(im, RADIUS)
    im.save(strcomplete)

    os.remove(".\imgdone\cut.png")
    nb = nb + 1