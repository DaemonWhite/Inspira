from dataclasses import dataclass, field


@dataclass(frozen=True)
class TagCapability:
    present: bool = False
    stict: bool = False
    know: list = field(default_factory=list)
    know_nsfw: list = field(default_factory=list)


@dataclass(frozen=True)
class EndPointCapability:
    present: bool = False
    nsfw: bool = False
    tag: TagCapability = field(default_factory=TagCapability)
    limit_min: int = 1
    limit_max: int = 1
    timeout: int = 5
