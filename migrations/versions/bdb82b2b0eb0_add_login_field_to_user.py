"""add login field to user

Revision ID: bdb82b2b0eb0
Revises: 65fc9a43c23f
Create Date: 2016-04-05 21:40:25.272098

"""

# revision identifiers, used by Alembic.
revision = 'bdb82b2b0eb0'
down_revision = '65fc9a43c23f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('users', sa.Column('login', sa.String(length=63), nullable=False))
    op.create_unique_constraint(None, 'users', ['login'])


def downgrade():
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'login')
