# from email.message import EmailMessage
# import os, ssl, smtplib
# from dotenv import load_dotenv

# load_dotenv()

# MAIL_SENDER = os.getenv("MAIL_SENDER"),
# MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
# MAIL_FROM = os.getenv("MAIL_USERNAME"),
# MAIL_PORT = os.getenv("MAIL_PORT"),
# MAIL_SERVER = os.getenv("MAIL_SERVER"),
# MAIL_FROM_NAME="EduWAY",
# MAIL_STARTTLS = True,
# MAIL_SSL_TLS = False,
# USE_CREDENTIALS = True,
# VALIDATE_CERTS = True

# #######################


# subject = "Eduway"
# body = "Mail"

# em = EmailMessage()
# em['FROM'] = "noreply.pashayevsproject@gmail.com"
# em['TO'] = "pashayevler@gmail.com"
# em['SUBJECT'] = subject
# em.set_content(body)

# context = ssl.create_default_context()

# with smtplib.SMTP_SSL('smtp.gmail.com', 465, context) as smtp:
#     smtp.login("noreply.pashayevsproject@gmail.com", 'noreplynoreply1')
#     smtp.sendmail("noreply.pashayevsproject@gmail.com", "pashayevler@gmail.com", em.as_string())



import smtplib
from email.message import EmailMessage

email_address = "noreply.pashayevsproject@gmail.com"
email_password = "osblgjtmtwweqlaa"

msg = EmailMessage()
msg['Subject'] = "Email subject"
msg['From'] = email_address
msg['To'] = email_address
msg.set_content("This is email message")

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_address, email_password)
    smtp.send_message(msg)