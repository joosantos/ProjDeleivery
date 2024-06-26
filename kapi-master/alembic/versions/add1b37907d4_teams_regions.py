"""Teams regions

Revision ID: add1b37907d4
Revises: 027dcc5db289
Create Date: 2024-03-05 16:32:56.980769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add1b37907d4'
down_revision = '027dcc5db289'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teams', sa.Column('region', sa.String(), nullable=True))
    op.add_column('teams', sa.Column('district', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('teams', 'district')
    op.drop_column('teams', 'region')
    # ### end Alembic commands ###
