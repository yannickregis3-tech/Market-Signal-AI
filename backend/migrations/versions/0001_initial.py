"""Create initial market data and signal tables."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "instruments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("symbol", sa.String(40), nullable=False),
        sa.Column("display_name", sa.String(120), nullable=False),
        sa.Column("market_group", sa.String(32), nullable=False),
        sa.Column("provider", sa.String(60), nullable=True),
        sa.Column("quote_currency", sa.String(12), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_instruments_symbol", "instruments", ["symbol"], unique=True)
    op.create_index("ix_instruments_market_group", "instruments", ["market_group"])
    op.create_table(
        "candles",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("symbol", sa.String(40), nullable=False),
        sa.Column("timeframe", sa.String(12), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("received_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("provider", sa.String(60), nullable=False),
        sa.Column("open", sa.Float(), nullable=False),
        sa.Column("high", sa.Float(), nullable=False),
        sa.Column("low", sa.Float(), nullable=False),
        sa.Column("close", sa.Float(), nullable=False),
        sa.Column("volume", sa.Float(), nullable=True),
        sa.UniqueConstraint("symbol", "timeframe", "timestamp", name="uq_candle_symbol_tf_time"),
    )
    op.create_index("ix_candles_symbol", "candles", ["symbol"])
    op.create_index("ix_candles_symbol_tf_timestamp", "candles", ["symbol", "timeframe", "timestamp"])
    op.create_table(
        "scan_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("market_group", sa.String(32), nullable=False),
        sa.Column("timeframe", sa.String(12), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(24), nullable=False),
        sa.Column("instruments_scanned", sa.Integer(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=False),
    )
    op.create_index("ix_scan_runs_market_group", "scan_runs", ["market_group"])
    op.create_table(
        "signals",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("scan_run_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_runs.id"), nullable=True),
        sa.Column("symbol", sa.String(40), nullable=False),
        sa.Column("timeframe", sa.String(12), nullable=False),
        sa.Column("direction", sa.String(12), nullable=False),
        sa.Column("status", sa.String(24), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("entry", sa.Float(), nullable=True),
        sa.Column("stop_loss", sa.Float(), nullable=True),
        sa.Column("take_profits", sa.JSON(), nullable=False),
        sa.Column("rationale", sa.JSON(), nullable=False),
        sa.Column("data_timestamp", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_signals_symbol", "signals", ["symbol"])
    op.create_index("ix_signals_symbol_created", "signals", ["symbol", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_signals_symbol_created", table_name="signals")
    op.drop_index("ix_signals_symbol", table_name="signals")
    op.drop_table("signals")
    op.drop_index("ix_scan_runs_market_group", table_name="scan_runs")
    op.drop_table("scan_runs")
    op.drop_index("ix_candles_symbol_tf_timestamp", table_name="candles")
    op.drop_index("ix_candles_symbol", table_name="candles")
    op.drop_table("candles")
    op.drop_index("ix_instruments_market_group", table_name="instruments")
    op.drop_index("ix_instruments_symbol", table_name="instruments")
    op.drop_table("instruments")
