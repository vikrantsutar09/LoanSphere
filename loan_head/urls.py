from django.urls import path
from . import views

app_name = "loan_head"

urlpatterns = [
    path("", views.loan_head_dashboard, name="dashboard"),
    path("customer-requests/", views.loan_head_customer_requests, name="customer_requests"),
    path("documents/", views.loan_head_documents, name="documents"),
    path("login/", views.login, name="login"),
    path("logout/", views.loan_head_logout, name="logout"),
    path("register/", views.register, name="register"),
    path("update-loan/<int:loan_id>/<str:status>/", views.update_loan_status, name="update_loan"),
    path("update-document/<int:doc_id>/<str:status>/", views.update_document_status, name="update_document"),
    path("delete-loan/<int:loan_id>/", views.delete_loan, name="delete_loan"),
    path("emi/", views.loan_head_emi, name="emi_list"),

    path("report/", views.loan_head_report, name="report"),
    path("report/pdf/", views.loan_head_report_pdf, name="report_pdf"),
]