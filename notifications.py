import smtplib as smtplib


def send_notification(message):
    # message = message
    sender_email = " " # Replace with the Sender email
    password = " "
    receiver_email = " " # Replace with the Receiver email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
    print("mail sent")


