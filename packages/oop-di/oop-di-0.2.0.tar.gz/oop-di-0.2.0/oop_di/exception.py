class DependencyInjectionException(Exception):
    ...


class CircularImportException(DependencyInjectionException):
    ...


class DefinitionNotFound(DependencyInjectionException):
    ...
