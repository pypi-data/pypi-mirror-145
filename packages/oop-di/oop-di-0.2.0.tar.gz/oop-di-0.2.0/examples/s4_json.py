from pathlib import Path

from oop_di import ContainerDefinition, JsonExtension

from examples.s4_module import ProductService

container_definition = ContainerDefinition()
container_definition.add_extension(JsonExtension(Path(__file__).parent / "s4_config.json"))
container = container_definition.compile()


@container.inject()
def process_product_endpoint(something, *, product_service: ProductService):
    print(something)
    product_service.process_product()


process_product_endpoint("doing something before calling product service")
