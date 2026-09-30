from datetime import UTC, datetime


def get_utc_now() -> datetime:
    return datetime.now(UTC)
