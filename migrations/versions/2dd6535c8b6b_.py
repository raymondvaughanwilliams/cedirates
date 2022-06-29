"""empty message

Revision ID: 2dd6535c8b6b
Revises: 6accf57ebdf9
Create Date: 2022-05-11 09:52:17.446052

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2dd6535c8b6b'
down_revision = '6accf57ebdf9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meme', schema=None) as batch_op:
        batch_op.add_column(sa.Column('views', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meme', schema=None) as batch_op:
        batch_op.drop_column('views')

    # ### end Alembic commands ###
