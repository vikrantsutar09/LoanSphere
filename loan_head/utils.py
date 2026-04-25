import requests
from django.core.mail import send_mail
from django.conf import settings


# ✅ EMAIL FUNCTION
def send_loan_status_email(email, name, status):

    subject = f"Loan Status Update - {status}"

    message = f"""
Hello {name},

Your loan documents are {status}.

Thank you,
Smart Finance[LoanSphere]
"""

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


def send_sms(mobile, message):

    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = {
        "sender_id": "FSTSMS",
        "message": message,
        "language": "english",
        "route": "q",
        "numbers": str(mobile)
    }

    headers = {
        "authorization": settings.FAST2SMS_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        print("SMS RESPONSE:", response.json())
        return response.json()

    except Exception as e:
        print("SMS ERROR:", e)
        return None