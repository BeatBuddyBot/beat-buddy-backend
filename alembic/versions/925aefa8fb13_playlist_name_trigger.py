"""playlist name trigger

Revision ID: 925aefa8fb13
Revises: 656ae99ce97f
Create Date: 2025-10-03 20:04:59.831950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '925aefa8fb13'
down_revision: Union[str, Sequence[str], None] = '656ae99ce97f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
    CREATE OR REPLACE FUNCTION playlists_set_title_on_insert()
    RETURNS TRIGGER AS $$
    DECLARE
        playlist_count INT;
    BEGIN
        IF NEW.title IS NULL THEN
            SELECT COUNT(*) INTO playlist_count FROM playlists;
            NEW.title := 'New Playlist #' || (playlist_count + 1);
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trg_playlists_insert
    BEFORE INSERT ON playlists
    FOR EACH ROW
    EXECUTE FUNCTION playlists_set_title_on_insert();
    """)


def downgrade():
    op.execute("DROP TRIGGER IF EXISTS trg_playlists_insert ON playlists;")
    op.execute("DROP FUNCTION IF EXISTS playlists_set_title_on_insert;")
