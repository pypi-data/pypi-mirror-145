from abc import ABC, abstractmethod

from oop_di import ContainerDefinition, Extension

# #############Mailer bounded context###############


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


class MailExtension(Extension):
    def define(self):
        self.add_param("from_email", "test@example.com")
        self.add_named_service(MailerInterface, Mailer)


# ############Product bounded context###########


class ProductService:
    def __init__(self, mailer: MailerInterface):
        self.mailer = mailer

    def process_product(self):
        print("processing product")
        self.mailer.send_mail()


class ProductExtension(Extension):
    def define(self):
        self.add_service(ProductService)


# #################Application


container_definition = ContainerDefinition()
container_definition.add_extension(ProductExtension())
container_definition.add_extension(MailExtension())

container = container_definition.compile()


@container.inject()
def process_product_endpoint(something, *, product_service: ProductService):
    print(something)
    product_service.process_product()


process_product_endpoint("doing something before calling product service")
