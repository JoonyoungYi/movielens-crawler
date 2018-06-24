"""Add Amazon Movie and Rotten Movie relation

Revision ID: 1bdd0c54c957
Revises: 9c85ef82c3a7
Create Date: 2018-06-24 18:40:23.087613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bdd0c54c957'
down_revision = '9c85ef82c3a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rotten_movie', sa.Column('amazon_movie_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'rotten_movie', 'amazon_movie', ['amazon_movie_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'rotten_movie', type_='foreignkey')
    op.drop_column('rotten_movie', 'amazon_movie_id')
    # ### end Alembic commands ###
