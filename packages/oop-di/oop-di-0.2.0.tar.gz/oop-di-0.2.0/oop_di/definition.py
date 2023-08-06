from typing import Callable, Dict, List

from .types import NameType


class Definition:
    def __init__(
        self, name: NameType, factory: Callable, bindings: Dict[str, NameType], is_singleton: bool, tags: List[str]
    ):
        self.name = name
        self.factory = factory
        self.bindings = bindings
        self.is_singleton = is_singleton
        self.tags = tags
