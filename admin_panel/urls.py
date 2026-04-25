from django.urls import path
from . import views


app_name = "admin_panel"

urlpatterns = [

    path("", views.dashboard, name="dashboard"),

    path("loan-heads/", views.loan_head_list, name="loan_head_list"),
    path("loan-heads/create/", views.loan_head_create, name="loan_head_create"),
    path("loan-heads/edit/<int:pk>/", views.loan_head_edit, name="loan_head_edit"),
    path("loan-heads/delete/<int:pk>/", views.loan_head_delete, name="loan_head_delete"),
    path("loan-heads/report/", views.loan_head_report, name="loan_head_report"),
    path("loan-heads/export-excel/", views.loan_head_export_excel, name="loan_head_export_excel"),

    path("categories/", views.category_list, name="category_list"),
    path("categories/create/", views.category_create, name="category_create"),
    path("categories/edit/<int:pk>/", views.category_edit, name="category_edit"),
    path("categories/delete/<int:pk>/", views.category_delete, name="category_delete"),
    path("categories/export-excel/", views.category_export_excel, name="category_export_excel"),

    path("packages/", views.package_list, name="package_list"),
    path("packages/create/", views.package_create, name="package_create"),
    path("packages/<int:pk>/edit/", views.package_edit, name="package_edit"),
    path("packages/<int:pk>/delete/", views.package_delete, name="package_delete"),
    path("loan-packages/export-excel/", views.package_export_excel, name="package_export_excel"),

    path("login/", views.admin_login, name="login"),
    path("logout/", views.admin_logout, name="logout"),

    path("contacts/", views.contact_list, name="contact_list"),
    path("contacts/delete/<int:pk>/", views.contact_delete, name="contact_delete"),
    # path("register/", views.admin_register, name="register"),

    path('report/', views.admin_report, name='admin_report'),
    path('report/pdf/', views.admin_report_pdf, name='admin_report_pdf'),
]