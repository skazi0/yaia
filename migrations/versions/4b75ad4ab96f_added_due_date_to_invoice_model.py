"""added due date to invoice model

Revision ID: 4b75ad4ab96f
Revises: f803eda7c3aa
Create Date: 2016-04-20 21:37:14.077107

"""

# revision identifiers, used by Alembic.
revision = '4b75ad4ab96f'
down_revision = 'f803eda7c3aa'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('invoices', sa.Column('due_on', sa.DateTime(), nullable=False))


def downgrade():
    op.drop_column('invoices', 'due_on')
