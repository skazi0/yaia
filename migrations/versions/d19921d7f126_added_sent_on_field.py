"""added sent_on field

Revision ID: d19921d7f126
Revises: 534381d04908
Create Date: 2016-08-11 12:11:11.940043

"""

# revision identifiers, used by Alembic.
revision = 'd19921d7f126'
down_revision = '534381d04908'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('invoices', sa.Column('sent_on', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('invoices', 'sent_on')
