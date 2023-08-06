from abc import ABC, abstractmethod
from typing import List

from oop_di import ContainerDefinition


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


class MultiMailer(MailerInterface):
    def __init__(self, mailers: List[MailerInterface]):
        self.mailers = mailers

    def send_mail(self):
        for mailer in self.mailers:
            mailer.send_mail()


class ProductService:
    def __init__(self, mailer: MailerInterface):
        self.mailer = mailer

    def process_product(self):
        print("processing product")
        self.mailer.send_mail()


container_definition = ContainerDefinition()
container_definition.add_service(ProductService)

container_definition.add_param("test1_email", "test@example.com")
container_definition.add_named_service("admin1_mailer", Mailer, from_email="test1_email", tags=["admin_mailers"])
container_definition.add_param("test2_email", "test2@example.com")
container_definition.add_named_service("admin2_mailer", Mailer, from_email="test2_email", tags=["admin_mailers"])
container_definition.add_param("test3_email", "test3@example.com")
container_definition.add_named_service("admin3_mailer", Mailer, from_email="test3_email", tags=["admin_mailers"])

container_definition.add_named_service(MailerInterface, MultiMailer, mailers="#admin_mailers")

container = container_definition.compile()


@container.inject()
def process_product_endpoint(something, *, product_service: ProductService):
    print(something)
    product_service.process_product()


process_product_endpoint("doing something before calling product service")
