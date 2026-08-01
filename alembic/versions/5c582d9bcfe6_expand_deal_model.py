"""expand deal model

Revision ID: 5c582d9bcfe6
Revises: a053c3c86ed8
Create Date: 2026-08-01 08:30:39.045127

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5c582d9bcfe6"
down_revision: Union[str, Sequence[str], None] = "a053c3c86ed8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "deals",
        sa.Column(
            "property_id",
            sa.String(),
            nullable=False,
        ),
    )

    op.add_column(
        "deals",
        sa.Column(
            "city",
            sa.String(),
            nullable=True,
        ),
    )

    op.add_column(
        "deals",
        sa.Column(
            "state",
            sa.String(),
            nullable=True,
        ),
    )

    op.add_column(
        "deals",
        sa.Column(
            "zip_code",
            sa.String(),
            nullable=True,
        ),
    )

    op.add_column(
        "deals",
        sa.Column(
            "purchase_price",
            sa.Float(),
            nullable=True,
        ),
    )

    op.add_column(
        "deals",
        sa.Column(
            "estimated_value",
            sa.Float(),
            nullable=True,
        ),
    )

    op.add_column(
        "deals",
        sa.Column(
            "repair_cost",
            sa.Float(),
            nullable=True,
        ),
    )

    op.add_column(
        "deals",
        sa.Column(
            "projected_profit",
            sa.Float(),
            nullable=True,
        ),
    )

    op.add_column(
        "deals",
        sa.Column(
            "deal_score",
            sa.Float(),
            nullable=True,
        ),
    )

    op.add_column(
        "deals",
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    op.add_column(
        "deals",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    op.create_index(
        op.f("ix_deals_property_id"),
        "deals",
        ["property_id"],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_deals_property_id"),
        table_name="deals",
    )

    op.drop_column(
        "deals",
        "updated_at",
    )

    op.drop_column(
        "deals",
        "created_at",
    )

    op.drop_column(
        "deals",
        "deal_score",
    )

    op.drop_column(
        "deals",
        "projected_profit",
    )

    op.drop_column(
        "deals",
        "repair_cost",
    )

    op.drop_column(
        "deals",
        "estimated_value",
    )

    op.drop_column(
        "deals",
        "purchase_price",
    )

    op.drop_column(
        "deals",
        "zip_code",
    )

    op.drop_column(
        "deals",
        "state",
    )

    op.drop_column(
        "deals",
        "city",
    )

    op.drop_column(
        "deals",
        "property_id",
    )