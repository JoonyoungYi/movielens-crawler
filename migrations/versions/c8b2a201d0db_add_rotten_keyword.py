"""Add Rotten Keyword

Revision ID: c8b2a201d0db
Revises: a6b4f1857b63
Create Date: 2018-06-21 17:12:00.314471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8b2a201d0db'
down_revision = 'a6b4f1857b63'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('rotten_keywords', sa.String(length=1000), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item', 'rotten_keywords')
    # ### end Alembic commands ###
