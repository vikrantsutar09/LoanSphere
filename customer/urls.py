from django.conf import settings
from django.urls import path
from . import views



urlpatterns = [

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.dashboard, name='dashboard'),

    # Loan
    path('apply-loan/', views.apply_loan, name='apply_loan'),
    path('loan-status/', views.loan_status, name='loan_status'),

    path('profile/', views.profile, name='profile'),
    path('documents/', views.documents, name='documents'),

    # Document Upload
    # path('upload-document/<int:loan_id>/', views.upload_document, name='upload_document'),

    # EMI
    path('emi-tracking/', views.emi_tracking, name='emi_tracking'),
    path('pay-emi/<int:emi_id>/', views.pay_emi, name='pay_emi'),
    path('payment/<int:emi_id>/', views.payment_page, name='payment_page'),
    path('process-payment/<int:emi_id>/', views.process_payment, name='process_payment'),
    path('emi-history/', views.emi_history, name='emi_history'),
    path('delete_document/<int:doc_id>/', views.delete_document, name='delete_document'),
    path('emi-receipt/<int:emi_id>/', views.download_emi_receipt, name='download_emi_receipt'),

]
