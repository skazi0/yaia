"""added invoice sequence counter to user

Revision ID: 318c0e7ee9e6
Revises: 76cfb65376ff
Create Date: 2016-04-25 19:33:56.360844

"""

# revision identifiers, used by Alembic.
revision = '318c0e7ee9e6'
down_revision = '76cfb65376ff'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('users', sa.Column('next_invoice_num', sa.Integer(), server_default='1', nullable=False))


def downgrade():
    op.drop_column('users', 'next_invoice_num')
