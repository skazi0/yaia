"""added paid_date to invoice model

Revision ID: df31ab078bb4
Revises: d19921d7f126
Create Date: 2017-01-20 09:30:12.875723

"""

# revision identifiers, used by Alembic.
revision = 'df31ab078bb4'
down_revision = 'd19921d7f126'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('invoices', sa.Column('paid_on', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('invoices', 'paid_on')
