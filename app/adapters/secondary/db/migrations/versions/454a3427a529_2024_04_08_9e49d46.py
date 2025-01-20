"""2024-04-08_9e49d46

Revision ID: 454a3427a529
Revises: a28e477ec739
Create Date: 2024-04-08 17:15:31.389963

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "454a3427a529"
down_revision: Union[str, None] = "a28e477ec739"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("hotels", "rooms_quantity", schema="booking")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "hotels",
        sa.Column("rooms_quantity", sa.INTEGER(), autoincrement=False, nullable=False),
        schema="booking",
    )
    # ### end Alembic commands ###