"""One-time migration: fix conversations_registry.db records whose
messages_json contains Pydantic repr strings instead of proper dicts.

Run with:  python -m scripts._fix_conversations_db
"""
import json
import re
import sqlite3
from pathlib import Path

_DB = Path(__file__).parent.parent / "data" / "memory" / "conversations_registry.db"


def _parse_repr(s: str) -> dict:
    """Parse a Pydantic model __str__ like: role='user' content='...' metadata=None"""
    meta_sep = s.rfind(" metadata=")
    rest = s[:meta_sep] if meta_sep >= 0 else s
    role_m = re.match(r"role='([^']*)'", rest)
    role = role_m.group(1) if role_m else "user"
    ci = rest.find("content='")
    content = rest[ci + len("content='"):-1] if ci >= 0 else ""
    return {"role": role, "content": content, "metadata": None}


def main() -> None:
    conn = sqlite3.connect(str(_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT id, messages_json FROM conversations").fetchall()
    fixed = 0
    for row in rows:
        msgs = json.loads(row["messages_json"] or "[]")
        if not msgs or isinstance(msgs[0], dict):
            continue  # already valid
        new_msgs = [_parse_repr(m) if isinstance(m, str) else m for m in msgs]
        conn.execute(
            "UPDATE conversations SET messages_json=? WHERE id=?",
            (json.dumps(new_msgs, ensure_ascii=False), row["id"]),
        )
        fixed += 1
        print(f"Fixed {row['id']}: {len(new_msgs)} messages")
        for m in new_msgs:
            print(f"  [{m['role']}] {m['content'][:80]!r}")
    conn.commit()
    conn.close()
    print(f"Migration complete — {fixed} record(s) fixed.")


if __name__ == "__main__":
    main()
