"""empty message

Revision ID: 1997e498c373
Revises: 669da637c855
Create Date: 2022-12-01 13:54:56.778419

"""

# revision identifiers, used by Alembic.
revision = '1997e498c373'
down_revision = '669da637c855'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('customers', sa.Column('notes', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('customers', 'notes')
