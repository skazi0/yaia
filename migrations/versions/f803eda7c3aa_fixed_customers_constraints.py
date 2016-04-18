"""fixed customers constraints

Revision ID: f803eda7c3aa
Revises: c4a9e4ab3bce
Create Date: 2016-04-18 22:30:03.225949

"""

# revision identifiers, used by Alembic.
revision = 'f803eda7c3aa'
down_revision = 'c4a9e4ab3bce'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_index('name', table_name='customers')
    op.drop_index('tax_id', table_name='customers')
    op.create_unique_constraint(None, 'customers', ['user_id', 'tax_id'])
    op.create_unique_constraint(None, 'customers', ['user_id', 'name'])


def downgrade():
    op.drop_constraint(None, 'customers', type_='unique')
    op.drop_constraint(None, 'customers', type_='unique')
    op.create_index('tax_id', 'customers', ['tax_id'], unique=True)
    op.create_index('name', 'customers', ['name'], unique=True)
