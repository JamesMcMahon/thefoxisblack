#!/usr/bin/env python
import os
import os.path
import re
import requests

from BeautifulSoup import BeautifulSoup
from itertools import count
from time import sleep


SAVE_DIR       = 'wallpapers'
RESOLUTION     = '1920x1200'
STOP_IF_EXISTS = True  # Set to False to download all files even if the file exists and True to stop when it finds where it left off.
START_PAGE     = 1  # Page number to start downloading from. Keep this on '1' if you want to download everything at the current resolution.


def get_backgrounds():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    path = os.path.abspath(SAVE_DIR)

    pattern = re.compile(r'.*%s\.jpg$' % RESOLUTION)

    # Download wallpapers using a single session, and retry when downloads fail.
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=3)
    session.mount('http://', adapter)

    try:
        c = 0
        for page in count(START_PAGE):
            downloaded, carry_on = get_images_from_page(
                'http://www.thefoxisblack.com/category/the-desktop-wallpaper-project/page/%s/' % page,
            session, pattern, path)
            c += downloaded
            if not carry_on:
                break;
    finally:
        session.close()

    return c


def get_images_from_page(url, session, pattern, path):
    soup = BeautifulSoup(session.get(url).text)
    wallpapers = soup.findAll('a', href=pattern)

    if not wallpapers:
        print 'Reached an empty page, stopping.'
        return 0, False
    else:
        c = 0
        for link in wallpapers:
            href = link['href']
            wallpaper = href[href.rfind('/')+1:]
            save_to = '%s/%s' % (path, wallpaper)
            exists = os.path.isfile(save_to)

            if STOP_IF_EXISTS and exists:
                print "%s already downloaded, stopping." % wallpaper
                return c, False
            elif not exists:
                response = session.get(href)
                with open(save_to, 'wb') as f:
                    f.write(response.content)
                c += 1
                print wallpaper

        sleep(2)

    sleep(2)
    return c, True


if __name__ == '__main__':
    c = get_backgrounds()
    print '\n%s' % (lambda c: 'Downloaded %d new wallpaper%s.' % (
        c, (lambda c: 's' if c>1 else '')(c))
        if c>0 else 'No new wallpapers were downloaded.')(c)
