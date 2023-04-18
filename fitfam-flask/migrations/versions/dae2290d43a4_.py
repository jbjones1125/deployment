"""empty message

Revision ID: dae2290d43a4
Revises: 
Create Date: 2022-12-04 17:24:40.625880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dae2290d43a4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('firstName', sa.String(length=50), nullable=False),
    sa.Column('lastName', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=62), nullable=False),
    sa.Column('nickname', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('Groups',
    sa.Column('groupId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('groupName', sa.String(length=20), nullable=False),
    sa.Column('groupOwner', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['groupOwner'], ['User.id'], ),
    sa.PrimaryKeyConstraint('groupId')
    )
    op.create_table('Posts',
    sa.Column('postId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('postDateTime', sa.String(length=255), nullable=False),
    sa.Column('poster', sa.Integer(), nullable=True),
    sa.Column('groupAssociation', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(length=4096), nullable=False),
    sa.Column('postTags', sa.String(length=255), nullable=True),
    sa.Column('postImage', sa.Text(length=50000), nullable=True),
    sa.Column('postLikes', sa.Integer(), nullable=True),
    sa.Column('postTitle', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['poster'], ['User.id'], ),
    sa.PrimaryKeyConstraint('postId')
    )
    op.create_table('Profile',
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('AboutMe', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['User.id'], ),
    sa.PrimaryKeyConstraint('userId')
    )
    op.create_table('SecurityQuestions',
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('Question1', sa.String(length=20), nullable=True),
    sa.Column('Answer1', sa.String(length=255), nullable=True),
    sa.Column('Question2', sa.String(length=20), nullable=True),
    sa.Column('Answer2', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['User.id'], ),
    sa.PrimaryKeyConstraint('userId')
    )
    op.create_table('GroupMembers',
    sa.Column('group', sa.Integer(), nullable=False),
    sa.Column('member', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group'], ['Groups.groupId'], ),
    sa.ForeignKeyConstraint(['member'], ['User.id'], ),
    sa.PrimaryKeyConstraint('group')
    )
    op.create_table('PostLikes',
    sa.Column('postId', sa.Integer(), nullable=False),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['postId'], ['Posts.postId'], ),
    sa.ForeignKeyConstraint(['userId'], ['User.id'], ),
    sa.PrimaryKeyConstraint('postId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('PostLikes')
    op.drop_table('GroupMembers')
    op.drop_table('SecurityQuestions')
    op.drop_table('Profile')
    op.drop_table('Posts')
    op.drop_table('Groups')
    op.drop_table('User')
    # ### end Alembic commands ###
