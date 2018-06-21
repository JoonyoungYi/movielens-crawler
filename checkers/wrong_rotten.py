from models import Session
from models import Item
from models import RottenMovie
from utils.item import get_query


def _is_same_name(item_name, rotten_movie_name):
    if item_name.lower() == rotten_movie_name.lower():
        return True

    query = get_query(item_name)
    if query.lower() == rotten_movie_name.lower():
        return True

    return False


session = Session()
for item in session.query(Item).filter(Item.rotten_movie_id.isnot(None)):
    rotten_movie = item.rotten_movie
    assert rotten_movie
    if _is_same_name(
            item.name,
            rotten_movie.name) and item.is_valid_year(rotten_movie.year):
        continue

    print('')
    print(item.year, item.release_date.year, item.name)
    print(rotten_movie.year, rotten_movie.name)

    # i = None
    # while i == 'y' or i == 'n':
    #     i = input('Is it right?')
    #     i = i.strip().lower()

    # if i == 'y':
    #
    # else:
    #     item.rotten_movie_id = None

    # items = _duplicated_items(session, item)
    #
    # if len(items) <= 0:
    #     continue
    #
    # print('   [*]', '{:4d}'.format(item.id), item.year, item.name)
    # for i in items:
    #     print('   [-]', '{:4d}'.format(i.id), i.year, i.name)
