#!/usr/bin/env python
import os
import os.path
import requests

from BeautifulSoup import BeautifulSoup as bs

MAX_PAGES = 1
SAVE_DIR = 'wallpapers'
RESOLUTION = '1280x800'

def get_backgrounds():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    base = 'http://www.thefoxisblack.com/category/the-desktop-wallpaper-project/page/%s/'
    c = 0
    for x in range(0, MAX_PAGES):
        c += get_images_from_page(base % (x + 1))

    return c


def get_images_from_page(url):
    html = fetchurl(url)
    soup = bs(html)
    c = 0
    for link in soup.findAll('a'):
        href = link['href']
        file_name = href[href.rfind('/'):]
        full_path = '%s%s' % (SAVE_DIR, file_name)
        if '-%s' % RESOLUTION in href and not os.path.isfile(full_path):
            print file_name[1:]
            r = requests.get(href)
            with open(full_path, 'wb') as f:
                f.write(r.content)
            c += 1

    return c


def fetchurl(url):
    return requests.get(url).text


if __name__ == '__main__':
    print '\nDownloaded %d new wallpapers.' % get_backgrounds()
