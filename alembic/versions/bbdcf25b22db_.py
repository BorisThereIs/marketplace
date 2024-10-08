"""empty message

Revision ID: bbdcf25b22db
Revises: c0707a6bcab1
Create Date: 2024-09-10 11:56:29.177892

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bbdcf25b22db'
down_revision: Union[str, None] = 'c0707a6bcab1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('sku', sa.String(length=64), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('shop_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.Column('price', sa.Numeric(scale=4), nullable=False),
    sa.Column('net_weight', sa.Double(precision=8), nullable=True),
    sa.Column('net_lenght', sa.Numeric(scale=2), nullable=True),
    sa.Column('net_width', sa.Numeric(scale=2), nullable=True),
    sa.Column('net_height', sa.Numeric(scale=2), nullable=True),
    sa.Column('gross_weight', sa.Double(precision=8), nullable=True),
    sa.Column('gross_lenght', sa.Numeric(scale=2), nullable=True),
    sa.Column('gross_width', sa.Numeric(scale=2), nullable=True),
    sa.Column('gross_height', sa.Numeric(scale=2), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sku', 'shop_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product')
    # ### end Alembic commands ###
