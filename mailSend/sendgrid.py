import sendgrid
import os
from sendgrid.helpers.mail import *
apikey = "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"
sg = sendgrid.SendGridAPIClient(apikey)

from_email = Email("test@example.com")
subject = "Hello World from the SendGrid Python Library!"

to_email = Email("b02507013@ntu.edu.tw")

content = Content("text/plain", "Hello, Email!")
mail = Mail(from_email, subject, to_email, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)