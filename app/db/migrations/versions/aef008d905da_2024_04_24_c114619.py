"""2024_04_24_c114619

Revision ID: aef008d905da
Revises: 454a3427a529
Create Date: 2024-04-24 14:55:18.500577

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aef008d905da"
down_revision: Union[str, None] = "454a3427a529"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "hotels", sa.Column("desc", sa.String(), nullable=True), schema="booking"
    )
    op.add_column(
        "rooms", sa.Column("name", sa.String(), nullable=True), schema="booking"
    )
    op.add_column(
        "rooms", sa.Column("desc", sa.String(), nullable=True), schema="booking"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("rooms", "desc", schema="booking")
    op.drop_column("rooms", "name", schema="booking")
    op.drop_column("hotels", "desc", schema="booking")
    # ### end Alembic commands ###
