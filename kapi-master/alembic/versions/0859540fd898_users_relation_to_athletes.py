"""Users relation to athletes

Revision ID: 0859540fd898
Revises: 899403b1c419
Create Date: 2024-01-14 17:20:28.750885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0859540fd898'
down_revision = '899403b1c419'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('athletes', sa.Column('user_id', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'athletes', 'users', ['user_id'], ['id'])
    op.add_column('users', sa.Column('athlete_id', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'users', 'athletes', ['athlete_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'athlete_id')
    op.drop_constraint(None, 'athletes', type_='foreignkey')
    op.drop_column('athletes', 'user_id')
    # ### end Alembic commands ###