from models import Session
from models import Item


def _duplicated_items(session, item):
    items = []
    for i in session.query(Item).filter_by(
            dataset=item.dataset,
            name=item.name,
            year=item.year,
            release_date=item.release_date, ).filter(Item.id > item.id):
        if i.video_release_date != item.video_release_date:
            continue
        if i.old_imdb_url != item.old_imdb_url:
            continue

        if i.original_item_id != item.id:
            items.append(i)
    return items


session = Session()
for item in session.query(Item):
    items = _duplicated_items(session, item)

    if len(items) <= 0:
        continue

    print('   [*]', '{:4d}'.format(item.id), item.year, item.name)
    for i in items:
        print('   [-]', '{:4d}'.format(i.id), i.year, i.name)
