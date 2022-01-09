"""Aggiunta campo immagine

Revision ID: d8027644c827
Revises: bdc6c38c6cf5
Create Date: 2022-01-08 11:39:32.554752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8027644c827'
down_revision = 'bdc6c38c6cf5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(length=120), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('image')

    # ### end Alembic commands ###
