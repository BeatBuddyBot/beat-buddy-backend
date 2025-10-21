"""some constraints

Revision ID: 1f27aadd0035
Revises: 925aefa8fb13
Create Date: 2025-10-22 01:12:26.751843

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1f27aadd0035'
down_revision: Union[str, Sequence[str], None] = '925aefa8fb13'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Playlist constraints
    op.create_check_constraint(
        "playlist_title_max_length",
        "playlists",
        "length(title) <= 70"
    )
    op.create_check_constraint(
        "playlist_description_max_length",
        "playlists",
        "length(description) <= 500"
    )

    # Song constraints
    op.create_check_constraint(
        "song_duration_non_negative",
        "songs",
        "duration >= 0"
    )


def downgrade() -> None:
    # Playlist constraints
    op.drop_constraint("playlist_title_max_length", "playlists", type_="check")
    op.drop_constraint("playlist_description_max_length", "playlists", type_="check")

    # Song constraints
    op.drop_constraint("song_duration_non_negative", "songs", type_="check")