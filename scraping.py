import requests
import bs4
import re
import os
import random
import errno

## Retrieve, name and download images from site on Max Burgmeier (Swiss painter)

LANDSCAPES_1_URL = "http://burgmeier.ch/index.php?show=Bilder&show2=&gallery_id=1&limit=0"
LANDSCAPES_2_URL = "http://burgmeier.ch/index.php?show=Bilder&show2=&gallery_id=1&limit=50"
LANDSCAPES_3_URL = "http://burgmeier.ch/index.php?show=Bilder&show2=&gallery_id=1&limit=100"
PORTRAITS_URL = "http://burgmeier.ch/index.php?show=Bilder&show2=&gallery_id=6"
STILL_LIFES_URL = "http://burgmeier.ch/index.php?show=Bilder&show2=&gallery_id=5"
URLS = [LANDSCAPES_1_URL, LANDSCAPES_2_URL, LANDSCAPES_3_URL, STILL_LIFES_URL, PORTRAITS_URL]

DIRECTORY_NAME = 'Burgmeier'

SEEN = [] # some images have identical titles

# example: "Max Burgmeier - Juralandschaft"
def get_picture_title(bs_selection):
    PICTURE_TITLE_BASE = "Max Burgmeier - "
    return PICTURE_TITLE_BASE + bs_selection.string.replace("/", "_")


# example: "http://burgmeier.ch/bilder/680.jpg"
def get_picture_url(bs_selection):
    PICTURE_URL_BASE = "http://burgmeier.ch/"
    return PICTURE_URL_BASE + re.sub('\_thumb', '', bs_selection.img['src'])


def mkdir(directory_name):
    path = os.getcwd() + "/" + directory_name
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def save_picture(picture_title, picture_url):
    if picture_title in SEEN:
            picture_title += " " + str(random.randint(0, 10))
    SEEN.append(picture_title)

    mkdir(DIRECTORY_NAME)

    response = requests.get(picture_url)
    if response.status_code == 200:
        with open(os.getcwd() + "/" + DIRECTORY_NAME + "/" + picture_title + ".jpg", 'wb') as f:
            f.write(response.content)
    else:
        print("There was a problem for " + picture_title + " at " + picture_url)


def save_pictures(pictures_page):
    CSS_CLASS_PICTURE_TITLE = "picture_title"
    CSS_CLASS_PICTURE_IMAGE = "picture2"

    pictures_soup = bs4.BeautifulSoup(requests.get(pictures_page).text, 'html.parser')

    for title, picture in zip(pictures_soup.find_all(class_=CSS_CLASS_PICTURE_TITLE),
                              pictures_soup.find_all(class_=CSS_CLASS_PICTURE_IMAGE)):
        save_picture(get_picture_title(title), get_picture_url(picture))


def main():
    print("Starting.")
    for picture_page in URLS:
        save_pictures(picture_page)
    print("Done.")


if __name__ == "__main__":
    main()
