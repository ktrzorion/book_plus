"""empty message

Revision ID: f7b3bffac6eb
Revises: 7127a43b4ccd
Create Date: 2024-03-27 11:46:21.239849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7b3bffac6eb'
down_revision = '7127a43b4ccd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('issue_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contentId', sa.Integer(), nullable=False),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['contentId'], ['content.id'], ),
    sa.ForeignKeyConstraint(['userId'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('issue_request')
    # ### end Alembic commands ###
