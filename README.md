# Movielens Crawler

* The Project for Crawling Side Information Based on Movielens Dataset.

* Init
```
virtualenv .venv -p python3.6
. .venv/bin/activate
pip install -r requirements.txt
```

* How to change database model
```
alembic revision --autogenerate -m "< message >"
alembic upgrade head
```
