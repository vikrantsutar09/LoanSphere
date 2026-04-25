"""
URL configuration for smart_finance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name="index"),
    path("required_documents/", views.required_documents, name="required_documents"),
    path("loan-types/", views.loan_types, name="loan_types"),
    
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("emi-calculator/", views.emi_calculator, name="emi_calculator"),
    path("contact/", views.contact, name="contact"),
    path("loan-app-form/<int:pk>/", views.loan_app_form, name="loan_app_form"),


    path("admin-panel/", include("admin_panel.urls")),

    path("loan-head/", include("loan_head.urls")),

    path('admin/', admin.site.urls),
    path('api/', include('ai_module.urls')),

    path('customer-panel/', include('customer.urls')),
    path("check-login-apply/<int:pk>/", views.check_login_apply, name="check_login_apply"),


    # path('loans/', include('loans.urls')),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

