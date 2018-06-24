# from traceback import format_exc
#
# import requests
#
# from models import Session
# from models import AppleMovie
# from models import WebPage
#
#
# def __request(path):
#     try:
#         r = requests.get('https://itunes.apple.com/us/movie{}'.format(path))
#         return r.text
#     except:
#         print(format_exc())
#         return None
#
#
# def __save(key, text):
#     with open('cdn/{}.html'.format(key), 'w') as f:
#         f.write(text)
#         return True
#     return False
#
#
# def _request_and_save(key, path):
#     text = __request(path)
#     if not text:
#         return False
#
#     return __save(key, text)
#
#
# def main():
#     session = Session()
#
#     for idx, apple_movie in enumerate(
#             session.query(AppleMovie).filter(AppleMovie.web_page_id.is_(
#                 None))):
#         # if apple_movie.id < 1623:
#         #     continue
#
#         print(
#             '>>',
#             '{:4d}'.format(apple_movie.id), )
#         if not apple_movie.url:
#             continue
#
#         web_page = WebPage()
#         session.add(web_page)
#         apple_movie.web_page = web_page
#         session.commit()
#
#         success = _request_and_save(web_page.key, apple_movie.url)
#         if not success:
#             session.delete(web_page)
#             apple_movie.web_page = None
#             session.commit()
#             print('  [-] Fail')
#         else:
#             print('  [+] Success')
#
#         # break
#
#
# if __name__ == '__main__':
#     main()
import requests
from bs4 import BeautifulSoup

s = requests.Session()
r = s.get(
    'http://www.amazon.com/gp/product/B008Y6O61Q/ref=atv_feed_catalog?tag=rottetomao_aiv_mv-20',
)
soup = BeautifulSoup(r.text, "html5lib")
print(soup.prettify())
for form in  soup.find_all('form', 'dv-action-single'):
    print(form.prettify())
# print(div)
