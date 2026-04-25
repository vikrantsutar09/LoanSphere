import requests
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from datetime import datetime

def send_sms(phone, message):

    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = {
        "route": "q",
        "message": message,
        "language": "english",
        "flash": 0,
        "numbers": phone,
    }

    headers = {
        "authorization": "Om3IqnJUzYStylaH6LM1pwTgKh9oD82RCQPXjbAvxGVu70iFWdrX8hDNM9P7gBzCfGbaoi4KpOxmSWsu",  # 🔥 Replace this
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()




from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from datetime import datetime


def send_emi_email(email, name, emi):

    loan = emi.loan

    total_emis = loan.emi_set.count()
    paid_emis = loan.emi_set.filter(is_paid=True).count()
    pending_emis = total_emis - paid_emis

    subject = "EMI Payment Successful"

    text_content = "Your EMI payment is successful."

    html_content = f"""
    <div style="font-family: Arial; line-height:1.8;">

    <h2 style="color:#0d6efd;">EMI Payment Confirmation</h2>

    <p>Dear <b>{name}</b>,</p>

    <p>
    Your EMI payment has been successfully processed.
    </p>

    <hr>

    <p><b>Loan Account No:</b> XXXX{str(loan.id)[-4:]}</p>
    <p><b>Total Loan Amount:</b> ₹ {loan.amount:.2f}</p>
    <p><b>EMI Amount Paid:</b> ₹ {emi.amount:.2f}</p>
    <p><b>EMI Number:</b> {emi.emi_number}</p>
    <p><b>Payment Date:</b> {datetime.now().strftime("%d-%m-%Y")}</p>
    <p><b>Status:</b> <span style="color:green;">Successful</span></p>

    <hr>

    <p><b>Loan Type:</b> {loan.loan_type}</p>
    <p><b>Interest Rate:</b> {loan.interest_rate}%</p>
    <p><b>Bank Name:</b> {loan.bank}</p>

    <hr>

    <p><b>Total EMIs:</b> {total_emis}</p>
    <p><b>EMIs Paid:</b> {paid_emis}</p>
    <p><b>EMIs Pending:</b> {pending_emis}</p>

    <hr>

    <p>
    Thank you for your payment. Your timely payments help maintain a good credit history.
    </p>

    <p>
    If you need any assistance, feel free to contact our support team.
    </p>

    <br>

    <p>
    Warm regards,<br>
    <b>Smart Finance[LoanSphere]</b>
    </p>

    </div>
    """

    email_msg = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [email]
    )

    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()