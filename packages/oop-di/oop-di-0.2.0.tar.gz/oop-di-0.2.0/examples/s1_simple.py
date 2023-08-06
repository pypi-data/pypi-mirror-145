from abc import ABC, abstractmethod

from oop_di import ContainerDefinition


# ### Domain code
class MailerInterface(ABC):
    @abstractmethod
    def send_mail(self):
        ...


class Mailer(MailerInterface):
    def __init__(self, from_email):
        self.from_email = from_email

    def send_mail(self):
        print(f"Sending from {self.from_email}...")
        print("Sent")


class ProductService:
    def __init__(self, mailer: MailerInterface):
        self.mailer = mailer

    def process_product(self):
        print("processing product")
        self.mailer.send_mail()


# ### Container definition
container_definition = ContainerDefinition()
container_definition.add_param("from_email", "test@example.com")
container_definition.add_service(ProductService)
container_definition.add_named_service(MailerInterface, Mailer)

container = container_definition.compile()


# ### Application code


@container.inject()
def process_product_endpoint_or_something(something, *, product_service: ProductService):
    print(something)
    product_service.process_product()


process_product_endpoint_or_something("doing something before calling product service")
