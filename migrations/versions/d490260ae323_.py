"""empty message

Revision ID: d490260ae323
Revises: 04c63c25c607
Create Date: 2022-07-29 17:42:27.054254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd490260ae323'
down_revision = '04c63c25c607'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'Venue', ['phone'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Venue', type_='unique')
    # ### end Alembic commands ###