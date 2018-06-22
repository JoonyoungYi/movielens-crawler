from models import Session
from models import Item
from models import RottenMovie


def _filter_items(items):
    ids = set(i.original_item_id if i.original_item_id else i.id
              for i in items)
    return [i for i in items if i.id in ids]


session = Session()
for rotten_movie in session.query(RottenMovie):
    items = rotten_movie.items.all()
    if len(items) == 0:
        # raise NotImplementedError('RottenMovie 모델을 지우는 코드를 작성해야 합니다.')
        session.delete(rotten_movie)
        session.commit()
    elif len(items) == 1:
        continue

    items = _filter_items(items)
    if len(items) <= 1:
        continue

    print(
        '\n>>',
        '{:4d}'.format(rotten_movie.id),
        rotten_movie.year,
        rotten_movie.name,
        len(items), )
    for item in items:
        print(
            '   [*]',
            '{:4d}'.format(item.id),
            item.get_valid_years(),
            item.get_pretty_name(), )
