"""empty message

Revision ID: aeeb4e6e748b
Revises: bbace1dacd9b
Create Date: 2024-09-25 19:55:20.363268

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aeeb4e6e748b'
down_revision: Union[str, None] = 'bbace1dacd9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shipping_address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('is_default_address', sa.Boolean(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=50), nullable=False),
    sa.Column('state', sa.String(length=50), nullable=True),
    sa.Column('postal_code', sa.String(length=100), nullable=True),
    sa.Column('addressee', sa.String(length=100), nullable=False),
    sa.Column('address_1', sa.String(), nullable=False),
    sa.Column('address_2', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shipping_address')
    # ### end Alembic commands ###
