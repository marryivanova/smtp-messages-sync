"""create tables

Revision ID: e9b6e7667be3
Revises:
Create Date: 2025-08-15 18:19:03.236560

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e9b6e7667be3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String, unique=True, nullable=False),
        sa.Column("email", sa.String, unique=True, nullable=False),
    )

    op.create_table(
        "sale",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("sale_id", sa.Integer(), nullable=True),
        sa.Column("sale_description", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["sale_id"], ["sale.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "discounts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("promo_code", sa.String(), nullable=True),
        sa.Column("sale_id", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["sale_id"], ["sale.id"], ondelete="SET NULL"),
    )


def downgrade() -> None:
    op.drop_table("discounts")
    op.drop_table("sale")
    op.drop_table("user")
