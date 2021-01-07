"""remove next invoice number from user

Revision ID: 5653f0c8b683
Revises: 2d70356c6c5f
Create Date: 2021-01-08 00:37:32.920268

"""

# revision identifiers, used by Alembic.
revision = '5653f0c8b683'
down_revision = '2d70356c6c5f'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'next_invoice_num')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('next_invoice_num', mysql.INTEGER(display_width=11), server_default=sa.text('1'), autoincrement=False, nullable=False))
    ### end Alembic commands ###
