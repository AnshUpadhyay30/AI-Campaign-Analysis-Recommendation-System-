from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except Exception:  # pragma: no cover - optional dependency fallback
    yaml = None


@dataclass
class SkillDefinition:
    name: str
    description: str
    owner: str


def load_skill_definitions(base_dir: Path = Path("skills")) -> list[SkillDefinition]:
    definitions: list[SkillDefinition] = []
    if not base_dir.exists():
        return definitions

    for definition_path in base_dir.glob("*/definition.yaml"):
        if yaml is None:
            data = {}
        else:
            data = yaml.safe_load(definition_path.read_text(encoding="utf-8")) or {}
        definitions.append(
            SkillDefinition(
                name=str(data.get("name", definition_path.parent.name)),
                description=str(data.get("description", "")),
                owner=str(data.get("owner", "performance_intelligence")),
            )
        )
    return definitions
