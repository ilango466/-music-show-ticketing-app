from flask_mail import Message, Mail
from  music_app import app
from traceback import print_exc
import smtplib
from email.mime.text import MIMEText

mail = Mail(app)


def send_mail(subject, body, reciever):

    # Create a MIMEText object for the email content
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = app.config["MAIL_USERNAME"]
    msg['To'] = reciever

    try:
        # Connect to the SMTP server (you'll need the SMTP server address and port)
        server = smtplib.SMTP(app.config["MAIL_SERVER"], app.config["MAIL_PORT"])
        server.starttls()

        # Log in to your email account
        server.login(app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])

        # Send the email
        server.sendmail(app.config["MAIL_USERNAME"], reciever, msg.as_string())

        # Disconnect from the server
        server.quit()

        print("Email sent successfully")

    except Exception as e:
        print(f"Error: {e}")
