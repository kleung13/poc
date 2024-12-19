"""Add total_calories column to WorkoutModel

Revision ID: 7d9eaf373371
Revises: 1163a9927bef
Create Date: 2024-12-19 14:08:22.201924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d9eaf373371'
down_revision = '1163a9927bef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('workouts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_calories', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('workouts', schema=None) as batch_op:
        batch_op.drop_column('total_calories')

    # ### end Alembic commands ###
