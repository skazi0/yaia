"""added user address and tax id

Revision ID: 1456f2fb7ff4
Revises: ab5107c55199
Create Date: 2016-08-04 13:57:46.631832

"""

# revision identifiers, used by Alembic.
revision = '1456f2fb7ff4'
down_revision = 'ab5107c55199'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('users', sa.Column('address', sa.Text(), nullable=False))
    op.add_column('users', sa.Column('tax_id', sa.String(length=63), nullable=True))


def downgrade():
    op.drop_column('users', 'tax_id')
    op.drop_column('users', 'address')
