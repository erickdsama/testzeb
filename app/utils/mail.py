import os
from typing import List

import sendgrid
from sendgrid.helpers.mail import *


def send_mail(emails: List[str], subject_: str, content_: str):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("no-reply@zeb-test.com")
    to_emails = emails
    mail = Mail(from_email, to_emails=to_emails, subject=subject_, plain_text_content=Content("text/plain", content_))
    a = sg.client.mail.send.post(request_body=mail.get())
