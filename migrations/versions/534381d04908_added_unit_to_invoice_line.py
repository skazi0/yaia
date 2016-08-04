"""added unit to invoice line

Revision ID: 534381d04908
Revises: 101c0187567a
Create Date: 2016-08-04 14:14:57.827230

"""

# revision identifiers, used by Alembic.
revision = '534381d04908'
down_revision = '101c0187567a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('lines', sa.Column('unit', sa.String(length=10), nullable=False))


def downgrade():
    op.drop_column('lines', 'unit')
