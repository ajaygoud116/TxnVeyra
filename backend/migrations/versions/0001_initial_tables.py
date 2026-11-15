"""Create source record and import run tables."""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "import_runs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("source_dataset", sa.String(length=32), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("file_sha256", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False),
        sa.Column("rows_received", sa.Integer(), nullable=False),
        sa.Column("rows_inserted", sa.Integer(), nullable=False),
        sa.Column("rows_skipped", sa.Integer(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_import_runs_source_dataset", "import_runs", ["source_dataset"])
    op.create_index("ix_import_runs_file_sha256", "import_runs", ["file_sha256"])

    op.create_table(
        "source_records",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("source_dataset", sa.String(length=32), nullable=False),
        sa.Column("source_record_id", sa.String(length=255), nullable=False),
        sa.Column("event_timestamp", sa.DateTime(timezone=True), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("ingested_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("source_dataset", "source_record_id", name="uq_source_record_identity"),
    )
    op.create_index(
        "ix_source_records_dataset_timestamp",
        "source_records",
        ["source_dataset", "event_timestamp"],
    )


def downgrade() -> None:
    op.drop_index("ix_source_records_dataset_timestamp", table_name="source_records")
    op.drop_table("source_records")
    op.drop_index("ix_import_runs_file_sha256", table_name="import_runs")
    op.drop_index("ix_import_runs_source_dataset", table_name="import_runs")
    op.drop_table("import_runs")
