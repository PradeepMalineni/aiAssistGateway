import json
from pathlib import Path
def write_json(obj, path: str):
    p=Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2))
