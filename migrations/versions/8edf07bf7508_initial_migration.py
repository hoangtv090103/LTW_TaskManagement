"""Initial migration.

Revision ID: 8edf07bf7508
Revises: 
Create Date: 2023-11-02 21:54:39.105150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8edf07bf7508'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('role')
        batch_op.drop_column('group_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('group_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('role', sa.VARCHAR(length=100), nullable=True))
        batch_op.create_foreign_key(None, 'group', ['group_id'], ['id'])
        batch_op.drop_column('is_admin')

    # ### end Alembic commands ###