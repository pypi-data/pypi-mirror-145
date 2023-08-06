from abc import ABC, abstractmethod
from typing import List


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
