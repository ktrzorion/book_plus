"""empty message

Revision ID: 17d245d201e9
Revises: 242cc5001efb
Create Date: 2024-02-28 15:40:08.045170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17d245d201e9'
down_revision = '242cc5001efb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('content_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['content_id'], ['content.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rating')
    # ### end Alembic commands ###