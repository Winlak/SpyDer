from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('telegram_id', sa.BigInteger(), nullable=False, unique=True, index=True),
        sa.Column('is_premium', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_table(
        'accounts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('session_string', sa.Text()),
        sa.Column('status', sa.String(length=20)),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_table(
        'chats',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('chat_id', sa.String(length=128), index=True),
        sa.Column('title', sa.String(length=255)),
        sa.Column('is_favorite', sa.Boolean(), default=False),
        sa.Column('mode', sa.String(length=32)),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('chat_id', sa.Integer(), sa.ForeignKey('chats.id', ondelete='CASCADE')),
        sa.Column('external_message_id', sa.String(length=128), index=True),
        sa.Column('from_id', sa.String(length=128)),
        sa.Column('text', sa.Text()),
        sa.Column('media_type', sa.String(length=64)),
        sa.Column('media_url', sa.String(length=512)),
        sa.Column('created_at', sa.DateTime(timezone=True)),
        sa.Column('is_deleted', sa.Boolean(), default=False),
    )
    op.create_table(
        'message_edits',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('message_id', sa.Integer(), sa.ForeignKey('messages.id', ondelete='CASCADE')),
        sa.Column('old_text', sa.Text()),
        sa.Column('new_text', sa.Text()),
        sa.Column('edited_at', sa.DateTime(timezone=True)),
    )
    op.create_table(
        'deleted_messages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('message_id', sa.Integer(), sa.ForeignKey('messages.id', ondelete='CASCADE')),
        sa.Column('deleted_at', sa.DateTime(timezone=True)),
    )


def downgrade() -> None:
    op.drop_table('deleted_messages')
    op.drop_table('message_edits')
    op.drop_table('messages')
    op.drop_table('chats')
    op.drop_table('accounts')
    op.drop_table('users')
