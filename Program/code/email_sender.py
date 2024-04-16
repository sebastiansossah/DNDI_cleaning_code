import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText  # Import MIMEText
from email import encoders

def send_email(sender_email, sender_password, receiver_email, subject, body, files):
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach the body to the email
    message.attach(MIMEText(body, 'plain'))

    # Attach files
    for file in files:
        with open(file, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {file}")
        message.attach(part)

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # Use your email provider's SMTP server and port
    session.starttls()  # Enable security
    session.login(sender_email, sender_password)  # Login with your email and password
    text = message.as_string()
    session.sendmail(sender_email, receiver_email, text)
    session.quit()
    print('Mail Sent')


# send_email(sender_email, sender_password, receiver_email, subject, body, files)

