"""empty message

Revision ID: 86554dfa950a
Revises: f4fb221fdb7d
Create Date: 2022-06-29 03:43:06.859337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86554dfa950a'
down_revision = 'f4fb221fdb7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction_list', sa.Column('transaction_date', sa.Date(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transaction_list', 'transaction_date')
    # ### end Alembic commands ###
