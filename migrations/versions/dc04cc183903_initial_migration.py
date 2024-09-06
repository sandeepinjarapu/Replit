"""Initial migration

Revision ID: dc04cc183903
Revises: 
Create Date: 2024-09-06 05:20:57.026292

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer

# revision identifiers, used by Alembic.
revision = 'dc04cc183903'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add email and password_hash columns as nullable first
    with op.batch_alter_table('leaders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=True))

    # Create a temporary table reference
    leaders_table = table('leaders',
        column('id', Integer),
        column('email', String)
    )

    # Update existing rows with unique emails
    connection = op.get_bind()
    results = connection.execute(sa.select(leaders_table.c.id)).fetchall()
    for i, (id,) in enumerate(results):
        connection.execute(
            leaders_table.update().
            where(leaders_table.c.id == id).
            values(email=f'user{i+1}@example.com')
        )

    # Now make the email column non-nullable and add the unique constraint
    with op.batch_alter_table('leaders', schema=None) as batch_op:
        batch_op.alter_column('email', nullable=False)
        batch_op.create_unique_constraint('uq_leaders_email', ['email'])

def downgrade():
    with op.batch_alter_table('leaders', schema=None) as batch_op:
        batch_op.drop_constraint('uq_leaders_email', type_='unique')
        batch_op.drop_column('password_hash')
        batch_op.drop_column('email')
        