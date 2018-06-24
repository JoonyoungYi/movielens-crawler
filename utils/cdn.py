from traceback import format_exc

from bs4 import BeautifulSoup


def get_soup_from_web_page(web_page):
    try:
        with open('cdn/{}.html'.format(web_page.key), 'r') as f:
            soup = BeautifulSoup(f.read(), "html5lib")
            return soup
    except:
        # print(format_exc())
        pass
    return None


def save_to_cdn(key, text):
    with open('cdn/{}.html'.format(key), 'w') as f:
        f.write(text)
        return True
    return False
