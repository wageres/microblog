"""followers

Revision ID: 421da99e49e3
Revises: f6aff713447a
Create Date: 2020-09-27 21:50:44.349459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '421da99e49e3'
down_revision = 'f6aff713447a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
