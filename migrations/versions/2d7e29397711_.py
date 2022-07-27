"""empty message

Revision ID: 2d7e29397711
Revises: e599688a922d
Create Date: 2022-07-27 09:32:13.756918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d7e29397711'
down_revision = 'e599688a922d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'seeking_description')
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'website_link')
    # ### end Alembic commands ###
