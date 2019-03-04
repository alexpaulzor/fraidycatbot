from picamera import PiCamera
from time import sleep
from SimpleCV import Image, Display, ImageSet
import os

camera = PiCamera()
disp = Display()
dirname = 'data'
bgdir = os.path.join(dirname, 'bg')
bgname = os.path.join(bgdir, 'img{}.jpg')
bgf = os.path.join(dirname, 'bg.jpg')
timg = os.path.join(dirname, 'timg.jpg')
oimg = os.path.join(dirname, 'oimg.jpg')

def save_picture(fname):
    try:
        camera.start_preview()
        sleep(1)
        camera.capture(fname)
        print("Captured to {}".format(fname))
    finally:
        camera.stop_preview()

def build_bg():
    if os.path.exists(bgf):
        print("{} exists".format(bgf))
        return Image(bgf)
    for n in range(20):
        pn = bgname.format(n)
        if not os.path.exists(pn):
            save_picture(pn)
    frames = ImageSet()
    frames.load(bgdir)
    img = Image(frames[0].size())
    nframes = len(frames)
    for frame in frames:
        img = img + (frame / nframes)
    img.save(bgf)
    img.save(disp)
    sleep(2)
    return img

bg = build_bg()

save_picture(timg)

# Get Image from camera
img = Image(timg)
img = img - bg
#blobs = img.findBlobs()
#blobs.draw(autocolor=True)
# Make image black and white
# img = img.binarize()
# Draw the text "Hello World" on image
# img.drawText("Hello World!")
# Show the image
# img.show()
img.save(oimg)
img.save(disp)
sleep(3)
