from picamera import PiCamera
from time import sleep
from SimpleCV import Image, Display, ImageSet
import os

BG_PICS = 10
MAX_PICS = 3000
FRAME_DELAY = 0.5
camera = PiCamera()
disp = Display()
dirname = 'data'
bgdir = os.path.join(dirname, 'bg')
bgname = os.path.join(bgdir, 'img{}.jpg')
bgf = os.path.join(dirname, 'bg.jpg')
oimg = os.path.join(dirname, 'oimg{}.jpg')

def save_picture(fname):
    #camera.start_preview()
    camera.capture(fname)
    print("Captured to {}".format(fname))

def get_bg():
    if os.path.exists(bgf):
        print("{} exists".format(bgf))
        return Image(bgf)
    return build_bg()

def build_bg():
    for n in range(BG_PICS):
        pn = bgname.format(n)
        save_picture(pn)
        sleep(FRAME_DELAY)
    camera.stop_preview()
    frames = ImageSet()
    frames.load(bgdir)
    img = Image(frames[0].size())
    nframes = len(frames)
    for frame in frames:
        img = img + (frame / nframes)
    img.save(bgf)
    return img

def show_img(img):
    camera.stop_preview()
    img.save(disp)
    sleep(FRAME_DELAY)

def main():
    bg = build_bg()
    show_img(bg)
    i = 0
    while True:
        fname = oimg.format(i % MAX_PICS)
        save_picture(fname)

        img = Image(fname)
        dimg = img - bg
        blobs = dimg.findBlobs()
        blobs.draw(autocolor=True)
        show_img(dimg)
        i += 1

if __name__ == '__main__':
    main()

