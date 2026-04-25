from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from matplotlib.style import context
from admin_panel.models import LoanHead   
from customer.models import Loan, Document
from collections import defaultdict
from customer.models import EMI
from .utils import send_loan_status_email
from .utils import send_sms
from django.contrib import messages
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.db.models import Q



# ---------------- REGISTER ----------------

def register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        # check if email already exists
        if LoanHead.objects.filter(email=email).exists():

            return redirect("loan_head:login")

        LoanHead.objects.create(
            name=name,
            email=email,
            phone=phone,
            password=password
        )

        return redirect("loan_head:login")

    return render(request, "loan_head/register.html")


# ---------------- LOGIN ----------------
def login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            loan_head = LoanHead.objects.get(email=email, password=password)

            request.session["loan_head_id"] = loan_head.id
            request.session["loan_head_email"] = loan_head.email

            return redirect("loan_head:dashboard")

        except LoanHead.DoesNotExist:
            return render(request, "loan_head/login.html", {
                "error": "Invalid email or password"
            })

    return render(request, "loan_head/login.html")



# ---------------- DASHBOARD ----------------

def loan_head_dashboard(request):

    if not request.session.get("loan_head_id"):
        return redirect("loan_head:login")

    total_requests = Loan.objects.count()

    approved_loans = Loan.objects.filter(status="Approved").count()
    documents_pending = Document.objects.filter(status="Pending").count()
    rejected_documents = Document.objects.filter(status="Rejected").count()

    context = {
        "total_requests": total_requests,
        "approved_loans": approved_loans,
        "documents_pending": documents_pending,
        "rejected_documents": rejected_documents,   
    }

    return render(request, "loan_head/loan_head_dashboard.html", context)


# ---------------- OTHER PAGES ----------------

def loan_head_customer_requests(request):

    if not request.session.get("loan_head_id"):
        return redirect("loan_head:login")

    loans = Loan.objects.all().order_by('-id')

    return render(request, "loan_head/loan_head_customer_request.html", {
        "loans": loans
    })

def delete_loan(request, loan_id):

    loan = get_object_or_404(Loan, id=loan_id)
    loan.delete()

    return redirect("loan_head:customer_requests")


def update_loan_status(request, loan_id, status):

    if not request.session.get("loan_head_id"):
        return redirect("loan_head:login")

    loan = get_object_or_404(Loan, id=loan_id)

    # UPDATE STATUS
    if status == "Approved":
        loan.status = "Approved"

        # 🔥 SEND EMAIL
        send_loan_status_email(
            loan.email,
            loan.full_name,
            "Approved"
        )

    elif status == "Rejected":
        loan.status = "Rejected"

        # 🔥 SEND EMAIL
        send_loan_status_email(
            loan.email,
            loan.full_name,
            "Rejected"
        )

    loan.save()

    return redirect("loan_head:customer_requests")


def loan_head_documents(request):

    if not request.session.get("loan_head_id"):
        return redirect("loan_head:login")

    documents = Document.objects.select_related(
        'loan', 'loan__customer'
    ).order_by('loan_id')   # 🔥 important

    grouped_data = defaultdict(list)

    for doc in documents:
        key = doc.loan.id   # ✅ FIX
        grouped_data[key].append(doc)

    return render(request, "loan_head/loan_head_document.html", {
        "grouped_documents": dict(grouped_data)
    })

    return render(request, "loan_head/loan_head_document.html", context)


def update_document_status(request, doc_id, status):

    doc = get_object_or_404(Document, id=doc_id)

    # update document
    doc.status = status
    doc.save()

    loan = doc.loan

    all_docs = Document.objects.filter(loan=loan)

    # ❌ IF ANY REJECTED
    if all_docs.filter(status="Rejected").exists():
        loan.status = "Rejected"

    # ⏳ IF STILL PENDING
    elif all_docs.exclude(status="Approved").exists():
        loan.status = "Pending"

    # ✅ ALL APPROVED
    else:
        loan.status = "Approved"

        # 🔥 SEND EMAIL
        send_loan_status_email(
            loan.email,
            loan.full_name,
            "Approved"
        )

        # 🔥 SEND SMS
        message = f"Hello {loan.full_name}, Your loan documents are approved successfully."

        send_sms(
            loan.mobile,
            message
        )

        # 🔥 SUCCESS MESSAGE (UI)
        messages.success(request, "📩 Email & SMS Sent Successfully!")

    loan.save()

    return redirect("loan_head:documents")


# ---------------- LOGOUT ----------------

def loan_head_logout(request):
    request.session.flush()
    auth_logout(request)
    return redirect("loan_head:login")




def loan_head_emi(request):

    if not request.session.get("loan_head_id"):
        return redirect("loan_head:login")

    emis = EMI.objects.select_related('loan', 'loan__customer').order_by('loan_id')

    total_emis = emis.count()
    pending_emis = emis.filter(is_paid=False).count()
    paid_emis = emis.filter(is_paid=True).count()

    # 🔥 GROUP BY LOAN (CUSTOMER WISE)
    grouped_emis = defaultdict(list)

    for emi in emis:
        key = emi.loan.id   # unique per customer loan
        grouped_emis[key].append(emi)

    context = {
        "grouped_emis": dict(grouped_emis),
        "total_emis": total_emis,
        "pending_emis": pending_emis,
        "paid_emis": paid_emis
    }

    return render(request, "loan_head/loan_head_emi.html", context)



from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO


# ================= REPORT =================
from django.db.models import Q

def loan_head_report(request):

    if not request.session.get("loan_head_id"):
        return redirect("loan_head:login")

    search = request.GET.get("search")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    loans = Loan.objects.all()
    documents = Document.objects.select_related('loan')
    emis = EMI.objects.select_related('loan')

    # 🔍 SEARCH FILTER
    if search:
        loans = loans.filter(
            Q(full_name__icontains=search) |
            Q(email__icontains=search)
        )

        documents = documents.filter(
            Q(loan__full_name__icontains=search) |
            Q(document_type__icontains=search)
        )

        emis = emis.filter(
            Q(loan__full_name__icontains=search)
        )

    if start_date:
        emis = emis.filter(due_date__gte=start_date)

    if end_date:
        emis = emis.filter(due_date__lte=end_date)

    context = {
        "loans": loans,
        "documents": documents,
        "emis": emis,
    }

    return render(request, "loan_head/loan_head_report.html", context)


# ================= PDF =================
def loan_head_report_pdf(request):

    from django.db.models import Q

    search = request.GET.get("search")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    loans = Loan.objects.all()
    documents = Document.objects.select_related('loan')
    emis = EMI.objects.select_related('loan')

    if search:
        loans = loans.filter(Q(full_name__icontains=search))
        documents = documents.filter(Q(loan__full_name__icontains=search))
        emis = emis.filter(Q(loan__full_name__icontains=search))

    # 📅 SAME DATE FILTER
    if start_date:
        emis = emis.filter(due_date__gte=start_date)

    if end_date:
        emis = emis.filter(due_date__lte=end_date)

    context = {
        "loans": loans,
        "documents": documents,
        "emis": emis,
    }

    template = get_template("loan_head/loan_head_report_pdf.html")
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="loan_head_report.pdf"'

    pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=response)

    return response