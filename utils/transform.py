import uuid
from datetime import datetime, timezone


def flatten(obj: dict, parent_key: str = "", sep: str = "_") -> dict[str, object]:
    items: dict[str, object] = {}
    for k, v in obj.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten(v, new_key, sep))
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    items.update(flatten(item, new_key, sep))
        else:
            items[new_key] = v
    return items


def to_record(raw: dict) -> dict[str, object]:
    record = flatten(raw)
    record["uuid"] = str(uuid.uuid4())
    record["insert_datetime"] = datetime.now(timezone.utc).isoformat()
    record.setdefault("wind_gust", None)
    return record
