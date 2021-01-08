"""add is_prepaid to invoice line

Revision ID: 669da637c855
Revises: 295e5a33f801
Create Date: 2021-01-08 12:27:58.210112

"""

# revision identifiers, used by Alembic.
revision = '669da637c855'
down_revision = '295e5a33f801'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import expression


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lines', sa.Column('is_prepaid', sa.Boolean(), nullable=False, server_default=expression.false()))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lines', 'is_prepaid')
    ### end Alembic commands ###
