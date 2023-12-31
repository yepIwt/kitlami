"""empty message

Revision ID: 4d9c29af0b1b
Revises:
Create Date: 2023-06-13 17:18:44.555323

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4d9c29af0b1b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("first_name", sa.VARCHAR(length=50), nullable=True),
        sa.Column("last_name", sa.VARCHAR(length=50), nullable=True),
        sa.Column("email", sa.VARCHAR(length=254), nullable=False),
        sa.Column("picture_url", sa.TEXT(), nullable=True),
        sa.Column("hashed_password", sa.TEXT(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
