"""pizza_type_sauce_feature

Revision ID: 2e0e797a89bf
Revises: 3465a4240791
Create Date: 2024-06-28 15:56:55.792808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e0e797a89bf'
down_revision = '3465a4240791'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pizza_type_sauce_quantity',
    sa.Column('pizza_type_id', sa.Uuid(), nullable=False),
    sa.Column('sauce_id', sa.Uuid(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pizza_type_id'], ['pizza_type.id'], ),
    sa.ForeignKeyConstraint(['sauce_id'], ['sauce.id'], ),
    sa.PrimaryKeyConstraint('pizza_type_id', 'sauce_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pizza_type_sauce_quantity')
    # ### end Alembic commands ###
