"""add playlist update triggers

Revision ID: c8e2da18784a
Revises: da7be1a2c1a5
Create Date: 2025-09-29 14:18:35.959200

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8e2da18784a'
down_revision: Union[str, Sequence[str], None] = 'da7be1a2c1a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE OR REPLACE FUNCTION touch_playlist_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            UPDATE playlists
            SET updated_at = NOW()
            WHERE id = NEW.playlist_id OR id = OLD.playlist_id;
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER song_after_insert
        AFTER INSERT ON songs
        FOR EACH ROW
        EXECUTE FUNCTION touch_playlist_updated_at();
    """)

    op.execute("""
        CREATE TRIGGER song_after_delete
        AFTER DELETE ON songs
        FOR EACH ROW
        EXECUTE FUNCTION touch_playlist_updated_at();
    """)


def downgrade():
    op.execute("DROP TRIGGER IF EXISTS song_after_insert ON songs;")
    op.execute("DROP TRIGGER IF EXISTS song_after_delete ON songs;")

    op.execute("DROP FUNCTION IF EXISTS touch_playlist_updated_at();")
