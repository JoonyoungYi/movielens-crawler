"""Add Item Original Id Column

Revision ID: a6b4f1857b63
Revises: d276909b9d20
Create Date: 2018-06-21 12:43:14.305409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6b4f1857b63'
down_revision = 'd276909b9d20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('original_item_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_item_original_item_id'), 'item', ['original_item_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_item_original_item_id'), table_name='item')
    op.drop_column('item', 'original_item_id')
    # ### end Alembic commands ###
