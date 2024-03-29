"""added account and account transfer

Revision ID: cd9107b53b39
Revises: 475b589348ff
Create Date: 2021-12-25 17:37:17.254301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd9107b53b39'
down_revision = '475b589348ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transaction_account',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('account_name', sa.String(length=128), nullable=False),
    sa.Column('account_type', sa.String(length=128), nullable=False),
    sa.Column('account_balance', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('account_owner', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transaction_account_transfer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('from_account_id', sa.Integer(), nullable=False),
    sa.Column('to_account_id', sa.Integer(), nullable=False),
    sa.Column('transfer_cost', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['from_account_id'], ['transaction_account.id'], ),
    sa.ForeignKeyConstraint(['to_account_id'], ['transaction_account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('transaction_list', sa.Column('transaction_account_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'transaction_list', 'transaction_account', ['transaction_account_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transaction_list', type_='foreignkey')
    op.drop_column('transaction_list', 'transaction_account_id')
    op.drop_table('transaction_account_transfer')
    op.drop_table('transaction_account')
    # ### end Alembic commands ###
