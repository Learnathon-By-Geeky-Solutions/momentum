"""add order model

Revision ID: a788847794e8
Revises: 01af711a72c8
Create Date: 2025-03-05 23:55:18.842546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a788847794e8'
down_revision: Union[str, None] = '01af711a72c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('order_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_index(op.f('ix_orders_order_id'), 'orders', ['order_id'], unique=False)
    op.create_table('bills',
    sa.Column('bill_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('method', sa.String(length=50), nullable=False),
    sa.Column('trx_id', sa.String(length=100), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('bill_id')
    )
    op.create_index(op.f('ix_bills_bill_id'), 'bills', ['bill_id'], unique=False)
    op.create_table('order_items',
    sa.Column('order_item_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('size', sa.String(length=50), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_id'], ['product.product_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('order_item_id')
    )
    op.create_index(op.f('ix_order_items_order_item_id'), 'order_items', ['order_item_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_order_items_order_item_id'), table_name='order_items')
    op.drop_table('order_items')
    op.drop_index(op.f('ix_bills_bill_id'), table_name='bills')
    op.drop_table('bills')
    op.drop_index(op.f('ix_orders_order_id'), table_name='orders')
    op.drop_table('orders')
    # ### end Alembic commands ###
