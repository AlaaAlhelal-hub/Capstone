"""empty message

Revision ID: f96da78320c0
Revises:
Create Date: 2020-12-23 22:43:16.608803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f96da78320c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    pass
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('movie_actor')
    # ### end Alembic commands ###


def downgrade():
    pass
    # ### commands auto generated by Alembic - please adjust! ###
    '''
    op.create_table('movie_actor',
    sa.Column('movies', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('actors', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['actors'], ['actors.id'], name='movie_actor_actors_fkey'),
    sa.ForeignKeyConstraint(['movies'], ['movies.id'], name='movie_actor_movies_fkey')
    )
    '''
    # ### end Alembic commands ###
