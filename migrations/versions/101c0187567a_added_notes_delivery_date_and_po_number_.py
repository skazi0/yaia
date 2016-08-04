"""added notes, delivery date and po number to invoice

Revision ID: 101c0187567a
Revises: 1456f2fb7ff4
Create Date: 2016-08-04 14:08:06.918047

"""

# revision identifiers, used by Alembic.
revision = '101c0187567a'
down_revision = '1456f2fb7ff4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('invoices', sa.Column('delivered_on', sa.DateTime(), nullable=False))
    op.add_column('invoices', sa.Column('notes', sa.Text(), nullable=False))
    op.add_column('invoices', sa.Column('po_num', sa.String(length=63), nullable=True))


def downgrade():
    op.drop_column('invoices', 'po_num')
    op.drop_column('invoices', 'notes')
    op.drop_column('invoices', 'delivered_on')
