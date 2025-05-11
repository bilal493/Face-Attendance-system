from email.message import EmailMessage
import ssl
import smtplib
from Backend.Email.parent_mail import fetch_parent_email  # Import fetch function

def send_email_notification():
    # Fetch parent's email
    email_reciever = fetch_parent_email()

    if email_reciever:
        email_sender = 'bilaltalha0095@gmail.com'
        email_password = 'mwvv kmwm dghe mymp'  # App password, keep this secret!

        subject = 'Student Entry Notification'
        body = "Your son/daughter has entered the university."

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_reciever
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_reciever, em.as_string())
            print(f"✅ Email sent to {email_reciever}")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
    else:
        print("❗ No parent email found. Email not sent.")
