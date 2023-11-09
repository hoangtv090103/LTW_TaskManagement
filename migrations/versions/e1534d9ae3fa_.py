"""empty message

Revision ID: e1534d9ae3fa
Revises: e56d5afd2ef9
Create Date: 2023-11-08 22:38:15.804160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1534d9ae3fa'
down_revision = 'e56d5afd2ef9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###