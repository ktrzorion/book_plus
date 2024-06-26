"""empty message

Revision ID: 841167ee0378
Revises: 0ac247a6136f
Create Date: 2024-02-29 13:43:30.814807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '841167ee0378'
down_revision = '0ac247a6136f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('borrowing', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_return_date', sa.DateTime(), nullable=True))
        batch_op.drop_column('extended_return_date')
        batch_op.drop_column('estimated_return_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('borrowing', schema=None) as batch_op:
        batch_op.add_column(sa.Column('estimated_return_date', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('extended_return_date', sa.DATETIME(), nullable=True))
        batch_op.drop_column('last_return_date')

    # ### end Alembic commands ###
