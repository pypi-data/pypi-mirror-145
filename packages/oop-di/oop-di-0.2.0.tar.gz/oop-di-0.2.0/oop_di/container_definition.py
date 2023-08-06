import inspect
from typing import Any, Callable, Dict, List

from .container import Container
from .definition import Definition
from .exception import CircularImportException, DefinitionNotFound
from .extension import Extension
from .types import NameType


class ContainerDefinition:
    def __init__(self):
        self._definitions: Dict[NameType, Definition] = {}
        self._params: Dict[NameType, Any] = {}
        self._in_compile: Dict[NameType, bool] = {}
        self._aliases: Dict[NameType, NameType] = {}

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

    def add_extension(self, extension: Extension):
        self._definitions.update(extension.get_definitions())
        self._aliases.update(extension.get_aliases())
        self._params.update(extension.get_params())

    def compile(self) -> Container:
        container = Container(self._params)
        for name in self._definitions.keys():
            self._compile_definition(name, container)

        for alias, service in self._aliases.items():
            container.add_alias(alias, service)

        return container

    def _compile_definition(self, name, container: Container):
        if name in self._aliases:
            return self._compile_definition(self._aliases[name], container)
        if name in self._params:
            return

        definition = self._definitions.get(name)
        if not definition:
            raise DefinitionNotFound(f"No definition for {name} found")
        if self._in_compile.get(definition.name, None):
            raise CircularImportException("Circular import error")

        self._in_compile[definition.name] = True
        if container.has(definition.name):
            self._in_compile.pop(definition.name)
            return

        self._resolve_dependencies(definition, container)
        container.add_service(
            definition.name,
            self._bind_factory_to_container(definition, container),
            definition.is_singleton,
            definition.tags,
        )

        self._in_compile.pop(definition.name)

    def _bind_factory_to_container(self, definition: Definition, container: Container):
        factory = definition.factory
        bindings = definition.bindings
        args = inspect.getfullargspec(factory)

        def bound_factory():
            arguments = []
            for arg_name in args.args:
                if arg_name == "self":
                    continue
                if binding := bindings.get(arg_name):
                    arguments.append(container.get(binding))
                    continue
                try:
                    arguments.append(
                        container.get(args.annotations[arg_name], raise_if_none=False) or container.get(arg_name)
                    )
                except KeyError:
                    arguments.append(container.get(arg_name))
            kwargs = {}
            for arg_name in args.kwonlyargs:
                if binding := bindings.get(arg_name):
                    kwargs[arg_name] = container.get(binding)
                    continue
                if args.kwonlydefaults and args.kwonlydefaults.get(arg_name):
                    d = args.kwonlydefaults.get(arg_name)
                    kwargs[arg_name] = d
                    continue

                try:
                    kwargs[arg_name] = container.get(args.annotations[arg_name], raise_if_none=False) or container.get(
                        arg_name
                    )
                except KeyError:
                    kwargs[arg_name] = container.get(arg_name)

            return factory(*arguments, **kwargs)

        return bound_factory

    def _resolve_dependencies(self, definition: Definition, container: Container):
        factory = definition.factory
        bindings = definition.bindings
        args = inspect.getfullargspec(factory)

        for arg_name in args.args:
            if arg_name == "self":
                continue

            if binding := bindings.get(arg_name):
                if isinstance(binding, str) and binding.startswith("#"):
                    continue
                self._compile_definition(binding, container)
                continue

            try:
                self._compile_definition(args.annotations[arg_name], container)
            except (KeyError, DefinitionNotFound):
                self._compile_definition(arg_name, container)
        for arg_name in args.kwonlyargs:
            if binding := bindings.get(arg_name):
                if isinstance(binding, str) and binding.startswith("#"):
                    continue
                self._compile_definition(binding, container)
                continue
            if args.kwonlydefaults and args.kwonlydefaults.get(arg_name):
                continue

            try:
                self._compile_definition(args.annotations[arg_name], container)
            except (KeyError, DefinitionNotFound):
                self._compile_definition(arg_name, container)
