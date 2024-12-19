"""empty message

Revision ID: d958dadc372b
Revises: 
Create Date: 2024-12-18 20:46:35.272348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd958dadc372b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bikes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('make', sa.String(), nullable=False),
    sa.Column('model', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('model')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('dimensions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stack', sa.Integer(), nullable=False),
    sa.Column('reach', sa.Integer(), nullable=False),
    sa.Column('seat_height', sa.Integer(), nullable=True),
    sa.Column('crank_length', sa.Integer(), nullable=True),
    sa.Column('size', sa.String(), nullable=False),
    sa.Column('bike_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['bike_id'], ['bikes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('bike_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['bike_id'], ['bikes.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('dimension_tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dimension_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dimension_id'], ['tags.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['dimensions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dimension_tags')
    op.drop_table('tags')
    op.drop_table('dimensions')
    op.drop_table('users')
    op.drop_table('bikes')
    # ### end Alembic commands ###
