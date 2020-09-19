"""quote_allowed add to news

Revision ID: b70458a3a914
Revises: 20553112b75f
Create Date: 2020-09-16 12:52:04.910346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b70458a3a914'
down_revision = '20553112b75f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('news', sa.Column('quote_allowed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('news', 'quote_allowed')
    # ### end Alembic commands ###
