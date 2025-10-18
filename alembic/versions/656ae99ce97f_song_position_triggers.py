"""song position triggers

Revision ID: 656ae99ce97f
Revises: ea21f0190e95
Create Date: 2025-10-03 19:18:33.250321

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '656ae99ce97f'
down_revision: Union[str, Sequence[str], None] = 'ea21f0190e95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # INSERT
    op.execute("""
    CREATE OR REPLACE FUNCTION songs_set_position_on_insert()
    RETURNS TRIGGER AS $$
    DECLARE
        max_pos INT;
    BEGIN
        SELECT COALESCE(MAX(position), -1) INTO max_pos
        FROM songs
        WHERE playlist_id = NEW.playlist_id;

        NEW.position := max_pos + 1;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trg_songs_insert
    BEFORE INSERT ON songs
    FOR EACH ROW
    EXECUTE FUNCTION songs_set_position_on_insert();
    """)

    # DELETE
    op.execute("""
    CREATE OR REPLACE FUNCTION songs_reorder_on_delete()
    RETURNS TRIGGER AS $$
    BEGIN
        IF pg_trigger_depth() > 1 THEN
            RETURN OLD;
        END IF;
        
        UPDATE songs
        SET position = position - 1
        WHERE playlist_id = OLD.playlist_id
          AND position > OLD.position;
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trg_songs_delete
    AFTER DELETE ON songs
    FOR EACH ROW
    EXECUTE FUNCTION songs_reorder_on_delete();
    """)

    # UPDATE
    op.execute("""
    CREATE OR REPLACE FUNCTION songs_reorder_on_update()
    RETURNS TRIGGER AS $$
    BEGIN
        IF pg_trigger_depth() > 1 THEN
            RETURN NEW;
        END IF;
        
        IF NEW.position < OLD.position THEN
            UPDATE songs
            SET position = position + 1
            WHERE playlist_id = NEW.playlist_id
              AND position >= NEW.position
              AND position < OLD.position
              AND id <> NEW.id;

        ELSIF NEW.position > OLD.position THEN
            UPDATE songs
            SET position = position - 1
            WHERE playlist_id = NEW.playlist_id
              AND position <= NEW.position
              AND position > OLD.position
              AND id <> NEW.id;
        END IF;

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trg_songs_update
    BEFORE UPDATE OF position ON songs
    FOR EACH ROW
    WHEN (OLD.position IS DISTINCT FROM NEW.position)
    EXECUTE FUNCTION songs_reorder_on_update();
    """)


def downgrade():
    op.execute("DROP TRIGGER IF EXISTS trg_songs_insert ON songs;")
    op.execute("DROP FUNCTION IF EXISTS songs_set_position_on_insert;")
    op.execute("DROP TRIGGER IF EXISTS trg_songs_delete ON songs;")
    op.execute("DROP FUNCTION IF EXISTS songs_reorder_on_delete;")
    op.execute("DROP TRIGGER IF EXISTS trg_songs_update ON songs;")
    op.execute("DROP FUNCTION IF EXISTS songs_reorder_on_update;")
