"""empty message

Revision ID: 015d4ad5c0fd
Revises: ef72f1bf6415
Create Date: 2024-03-23 11:41:18.243153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '015d4ad5c0fd'
down_revision = 'ef72f1bf6415'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('purchase_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('content_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['content_id'], ['content.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('purchase_data')
    # ### end Alembic commands ###
