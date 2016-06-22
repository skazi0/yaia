"""added invoice line model

Revision ID: ab5107c55199
Revises: 318c0e7ee9e6
Create Date: 2016-06-22 13:53:08.301888

"""

# revision identifiers, used by Alembic.
revision = 'ab5107c55199'
down_revision = '318c0e7ee9e6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('lines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invoice_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('quantity', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('unit_price', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('tax_rate', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('lines')
