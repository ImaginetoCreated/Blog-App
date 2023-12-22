import smtplib
from dotenv import load_dotenv
import os

# Todo 1 - Load Environmental Variables and set Constants
MY_EMAIL = os.getenv('MY_EMAIL')
MY_PASSWORD = os.getenv('MY_PASSWORD')
PORT = 587
GMAIL_SERVER = "smtp.gmail.com"


# Todo 2 - Create a Contact class
class Contact:
    def __init__(self, form_name, form_email, form_phone, form_message):
        self.username = form_name
        self.email = form_email
        self.phone = form_phone
        self.message = form_message
        self.form_to_email = self.prepare_message

    def prepare_message(self):
        '''Prepares a message to be sent'''
        sender_email = self.email
        sender_name = self.username
        sender_phone = self.phone
        sender_message = self.message
        email_subject = "Subject: Message from Blog User"
        email_body = f"""
                            Blogger Name: {sender_name}\n
                            Blogger Email: {sender_email}\n
                            Blogger Phone: {sender_phone}\n
                            Blogger Message: {sender_message}"""
        email_to_send = f"{email_subject} \n\n{email_body}"
        return email_to_send
    def send_message(self):
        sender_email = self.email
        sender_name = self.username
        sender_phone = self.phone
        sender_message = self.message
        email_subject = "Subject: Message from Blog User"
        email_body = f"""
                Blogger Name: {sender_name}\n 
                Blogger Email: {sender_email}\n 
                Blogger Phone: {sender_phone}\n 
                Blogger Message: {sender_message}"""
        try:
            with smtplib.SMTP(host=GMAIL_SERVER, port=PORT) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=self.email,
                    to_addrs=MY_EMAIL,
                    msg=f"{email_subject} \n\n{email_body}"
                )
            print("Sent email")
        except:
            print("Could not send email")

