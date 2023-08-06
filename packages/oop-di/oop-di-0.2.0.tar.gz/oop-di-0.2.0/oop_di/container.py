import inspect
from functools import partial
from typing import Any, Callable, Dict, List

from .service_builder import ServiceBuilder
from .types import NameType


class Container:
    def __init__(self, params):
        self._services: Dict[NameType, ServiceBuilder] = {}
        self._params: Dict[NameType, Any] = params
        self._aliases: Dict[NameType, NameType] = {}
        self._by_tag: Dict[str, List[NameType]] = {}

    def add_alias(self, alias: NameType, service: NameType):
        self._aliases[alias] = service

    def has(self, name: NameType):
        if self.get(name, raise_if_none=False):
            return True

        return False

    def get(self, name: NameType, raise_if_none: bool = True):
        if isinstance(name, str) and name.startswith("#"):
            return self.get_tagged(name[1:])
        if alias := self._aliases.get(name):
            return self.get(alias)

        if service := self._services.get(name):
            return service.get_instance()

        if param := self._params.get(name):
            return param

        if raise_if_none:
            raise Exception(f"Cannot find {name}")

        return None

    def add_service(self, name: NameType, factory: Callable[[], Any], is_singleton: bool = True, tags: List[str] = []):
        self._services[name] = ServiceBuilder(factory, is_singleton=is_singleton)
        for tag in tags:
            try:
                self._by_tag[tag].append(name)
            except KeyError:
                self._by_tag[tag] = [name]

    def get_tagged(self, tag: str):
        names = self._by_tag.get(tag)
        if not names:
            return []

        return [self.get(name) for name in names]

    def inject(self, *, ignore_missing=True, **bindings):
        container = self

        def wrapper(f):
            args = inspect.getfullargspec(f)
            kwargs = {}
            for arg_name in args.kwonlyargs:
                if binding := bindings.get(arg_name):
                    value = container.get(binding, raise_if_none=not ignore_missing)
                    if value:
                        kwargs[arg_name] = value
                    continue

                try:
                    value = container.get(args.annotations[arg_name], raise_if_none=False) or container.get(
                        arg_name, raise_if_none=not ignore_missing
                    )
                    if value:
                        kwargs[arg_name] = value
                except KeyError:
                    value = container.get(arg_name, raise_if_none=not ignore_missing)
                    kwargs[arg_name] = value

            return partial(f, **kwargs)

        return wrapper
