from models import Session
from models import Item
from models import RottenMovie

session = Session()
for rotten_movie in session.query(RottenMovie):
    items = rotten_movie.items.all()
    item_number = len(items)
    if item_number <= 1:
        assert item_number == 1
        continue

    print(
        '\n>>',
        '{:4d}'.format(rotten_movie.id),
        rotten_movie.year,
        rotten_movie.name,
        item_number, )
    for item in items:
        print('   [*]', '{:4d}'.format(item.id), item.year, item.name)
