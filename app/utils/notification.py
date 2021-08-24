from typing import List

from app.models import Product, ZbUser
from app.utils.mail import send_mail


def notify_product_change(admin_users: List[ZbUser], product: Product):

    emails = [admin.email for admin in admin_users]
    subject = f"Product {product.title} has changed"
    content = f"The product with id: {product.id} and title: {product.title} was changed"
    send_mail(emails, subject, content)
