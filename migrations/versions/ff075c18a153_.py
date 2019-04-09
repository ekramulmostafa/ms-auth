"""empty message

Revision ID: ff075c18a153
Revises: 2ffd80e1a1d3
Create Date: 2019-04-09 14:42:59.392148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff075c18a153'
down_revision = '2ffd80e1a1d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'verification_codes', ['code'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'verification_codes', type_='unique')
    # ### end Alembic commands ###
