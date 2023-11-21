"""empty message

Revision ID: 7e9d2f442a85
Revises: 650e0ec3e6f9
Create Date: 2023-11-17 16:27:17.998098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e9d2f442a85'
down_revision = '650e0ec3e6f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bills', schema=None) as batch_op:
        batch_op.drop_constraint('fk_bills_summary_id_summaries', type_='foreignkey')
        batch_op.drop_column('summary_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bills', schema=None) as batch_op:
        batch_op.add_column(sa.Column('summary_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_bills_summary_id_summaries', 'summaries', ['summary_id'], ['id'])

    # ### end Alembic commands ###
