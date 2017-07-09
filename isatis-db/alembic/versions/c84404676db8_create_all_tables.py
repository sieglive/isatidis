"""Create All Tables

Revision ID: c84404676db8
Revises: 
Create Date: 2017-07-09 00:29:54.571430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c84404676db8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('isatis_account',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=50), nullable=False),
    sa.Column('nick_name', sa.String(length=100), nullable=True),
    sa.Column('user_pass', sa.CHAR(length=32), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('permission', sa.SmallInteger(), nullable=True),
    sa.Column('avatar_path', sa.CHAR(length=255), nullable=True),
    sa.Column('active_status', sa.SmallInteger(), nullable=True),
    sa.Column('valid', sa.SmallInteger(), nullable=True),
    sa.Column('appear_time', sa.Integer(), nullable=False),
    sa.Column('register_time', sa.Integer(), nullable=False),
    sa.Column('expire_time', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_isatis_account_appear_time'), 'isatis_account', ['appear_time'], unique=False)
    op.create_index(op.f('ix_isatis_account_email'), 'isatis_account', ['email'], unique=True)
    op.create_index(op.f('ix_isatis_account_expire_time'), 'isatis_account', ['expire_time'], unique=False)
    op.create_index(op.f('ix_isatis_account_register_time'), 'isatis_account', ['register_time'], unique=False)
    op.create_index(op.f('ix_isatis_account_user_name'), 'isatis_account', ['user_name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_isatis_account_user_name'), table_name='isatis_account')
    op.drop_index(op.f('ix_isatis_account_register_time'), table_name='isatis_account')
    op.drop_index(op.f('ix_isatis_account_expire_time'), table_name='isatis_account')
    op.drop_index(op.f('ix_isatis_account_email'), table_name='isatis_account')
    op.drop_index(op.f('ix_isatis_account_appear_time'), table_name='isatis_account')
    op.drop_table('isatis_account')
    # ### end Alembic commands ###
