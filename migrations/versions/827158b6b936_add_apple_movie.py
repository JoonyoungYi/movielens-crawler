"""add apple_movie

Revision ID: 827158b6b936
Revises: b48d3707d548
Create Date: 2018-06-24 17:23:34.520635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '827158b6b936'
down_revision = 'b48d3707d548'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apple_movie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('web_page_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['web_page_id'], ['web_page.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('rotten_movie', sa.Column('apple_movie_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'rotten_movie', 'apple_movie', ['apple_movie_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'rotten_movie', type_='foreignkey')
    op.drop_column('rotten_movie', 'apple_movie_id')
    op.drop_table('apple_movie')
    # ### end Alembic commands ###