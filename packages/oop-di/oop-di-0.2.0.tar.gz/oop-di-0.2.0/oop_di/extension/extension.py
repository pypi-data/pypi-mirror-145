from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List

from ..definition import Definition
from ..types import NameType


class Extension(ABC):
    def __init__(self):
        self._definitions: Dict[NameType, Definition] = {}
        self._params: Dict[NameType, Any] = {}
        self._aliases: Dict[NameType, NameType] = {}
        self.define()

    def add_alias(self, alias: NameType, service: NameType):
        self._aliases[alias] = service

    def add_service(self, service: type, *, tags: List[str] = [], is_singleton=True, **bind):
        self._definitions[service] = Definition(service, service, bind, is_singleton=is_singleton, tags=tags)

    def add_named_service(self, name: NameType, service: type, *, tags: List[str] = [], is_singleton=True, **bind):
        self._definitions[name] = Definition(name, service, bind, is_singleton=is_singleton, tags=tags)

    def add_factory(self, name: NameType, factory: Callable, *, tags: List[str] = [], is_singleton=True, **bind):
        self._definitions[name] = Definition(name, factory, bind, is_singleton=is_singleton, tags=tags)

    def add_param(self, name: NameType, value: Any):
        self._params[name] = value

    def get_definitions(self) -> Dict[NameType, Definition]:
        return self._definitions

    def get_aliases(self) -> Dict[NameType, NameType]:
        return self._aliases

    def get_params(self) -> Dict[NameType, Any]:
        return self._params

    @abstractmethod
    def define(self):
        ...
