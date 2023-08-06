import importlib
from json import load
from pathlib import Path
from typing import Any, Dict, List

from ..types import NameType
from .extension import Extension


class JsonExtension(Extension):
    def __init__(self, json_path: Path):
        self.json_path = json_path
        super().__init__()

    def define(self):
        with open(self.json_path) as file:
            data = load(file)

        self._load_parameters(data.get("parameters", {}))
        self._load_aliases(data.get("aliases", {}))
        self._load_services(data.get("services", {}))
        importlib.invalidate_caches()

    def _load_parameters(self, data: Dict[str, Any]):
        for k, v in data.items():
            self.add_param(self._resolve_key(k), v)

    def _load_aliases(self, data: Dict[str, Any]):
        for k, v in data.items():
            self.add_alias(self._resolve_key(k), self._resolve_key(v))

    def _load_services(self, data: Dict[str, Any]):
        for k, v in data.items():
            self._load_module(k, v)

    def _load_module(self, mod: str, data: List[Dict[str, Any]]):
        for service in data:
            self._load_service(mod, service["class"], service)

    def _load_service(self, mod: str, item: str, data: Dict[str, Any]):
        service = self._resolve_key(f"@{mod}.{item}")
        parameters = {}
        for k, v in data.get("parameters", {}).items():
            parameters[k] = self._resolve_key(v)

        if name := data.get("name"):
            self.add_named_service(
                self._resolve_key(name),
                service,
                tags=data.get("tags", []),
                is_singleton=data.get("is_singleton", True),
                **parameters,
            )
        else:
            self.add_service(
                service, tags=data.get("tags", []), is_singleton=data.get("is_singleton", True), **parameters
            )
        for alias in data.get("aliases", []):
            self.add_alias(alias, service)

    def _resolve_key(self, key: str) -> NameType:
        if not key.startswith("@"):
            return key

        mod, class_name = key[1:].rsplit(".", 1)
        loaded = importlib.import_module(mod)

        return getattr(loaded, class_name)
