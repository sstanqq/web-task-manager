"""Create database

Revision ID: 94c0e21f421a
Revises:
Create Date: 2024-10-12 21:18:17.039681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94c0e21f421a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column(
                        'first_name', sa.String(length=50), nullable=False
                    ),
                    sa.Column('last_name', sa.Text(), nullable=True),
                    sa.Column(
                        'username', sa.String(length=50), nullable=False
                    ),
                    sa.Column(
                        'password', sa.String(length=100), nullable=False
                    ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('username'))
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('tasks',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=50), nullable=False),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('status', sa.Enum(
                            'NEW', 'IN_PROGRESS',
                            'COMPLETED', name='taskstatus'),
                        nullable=False
                    ),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['users.id'], ondelete='CASCADE'
                    ),
                    sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_table('tasks')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
