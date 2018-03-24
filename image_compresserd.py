#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, glob, re, time, sys
from PIL import Image

target_dir = "/path/to/dir/"
pattern = r"^(?!.*(_S|_M|_L).(jpg|jpeg|JPG)).*(jpg|jpeg|JPG)"
repattern = re.compile(pattern)


# 画像の中心を切り出す
def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

# 最大サイズのアスペクト比wratio:hratioの長方形を切り出す
def crop_max_rect(pil_img,wratio=1,hratio=1):
    w, h = pil_img.size
    if w * hratio > h * wratio:
        return crop_center(pil_img, h * wratio / hratio, h )
    else:
        return crop_center(pil_img, w , w * hratio / wratio)



def compress():
    paths = glob.glob(target_dir + '*')
    for path in paths:
        m = repattern.match(path)
        if m:
            img_path = m.group()
            img = Image.open(img_path)
            img_name, img_ext = os.path.splitext(img_path)

            # 既に圧縮されたものが存在すれば圧縮しない
            if os.path.exists(img_name+'_M'+img_ext) and os.path.exists(img_name+'_S'+img_ext):
                continue

            #img.save(img_name + '_L' + img_ext) #オリジナル（サイズ大）には'_L'
            crop_max_rect(img,3,2).resize((300,200)).save(img_name + '_M' + img_ext) #サイズ中'_M'
            crop_max_rect(img).resize((75,75)).save(img_name + '_S' + img_ext)       #サイズ小'_S'
            #os.remove(img_path) #オリジナルは削除
            img.close()

def loop():
    while 1:
        compress()
        time.sleep(10)


def fork():
    pid = os.fork()
    if pid > 0:
        f = open('/var/run/image_compresserd.pid','w')
        f.write(str(pid)+"\n")
        f.close()
        sys.exit()
    if pid == 0:
        loop()


if __name__=='__main__':
    fork()


