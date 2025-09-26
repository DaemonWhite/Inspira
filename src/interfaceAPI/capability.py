from dataclasses import dataclass, field

@dataclass(frozen=True)
class Capability:
    present: bool = False
    nsfw: bool = False
    know_tags: list = field(default_factory=list)
    limit_min: int = 1
    limit_max: int = 1
