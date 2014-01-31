#!/usr/bin/env python
import os
import os.path
import requests

from BeautifulSoup import BeautifulSoup as bs


MAX_PAGES = 50
SAVE_DIR = 'wallpapers'
RESOLUTION = '1280x800'
STOP_IF_EXISTS = True  # Set to False to download all files even if the file exists and True to stop when it finds where it left off.


def get_backgrounds():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    base = 'http://www.thefoxisblack.com/category/the-desktop-wallpaper-project/page/%s/'
    path = os.path.abspath(SAVE_DIR)
    c = 0
    for x in range(0, MAX_PAGES):
        downloaded, carry_on = get_images_from_page(base % (x + 1), path)
        c += downloaded
        if not carry_on:
            break;

    return c


def get_images_from_page(url, path):
    soup = bs(requests.get(url).text)
    c = 0
    for link in soup.findAll('a'):
        href = link['href']
        wallpaper = href[href.rfind('/')+1:]
        save_to = '%s/%s' % (path, wallpaper)
        exists = os.path.isfile(save_to)

        if STOP_IF_EXISTS and '-%s' % RESOLUTION in href and exists:
            print "%s already downloaded, stopping." % wallpaper
            return c, False
        elif '-%s' % RESOLUTION in href and not exists:
            print wallpaper
            r = requests.get(href)
            with open(save_to, 'wb') as f:
                f.write(r.content)
            c += 1

    return c, True


if __name__ == '__main__':
    c = get_backgrounds()
    print '\n%s' % (lambda c: 'Downloaded %d new wallpaper%s.' % (
        c, (lambda c: 's' if c>1 else '')(c))
        if c>0 else 'No new wallpapers were downloaded.')(c)
