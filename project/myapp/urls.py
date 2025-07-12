from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("", views.index_view, name="index"),
    path("logout/", views.logout_view, name='logout'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("upload/", views.upload_note, name="upload_to_drive"),
    path("view/", views.view_uploaded_files, name="view"),
    path("contact/", views.contact, name="contact"),
    path("whatsapp/", views.whatsapp, name="whatsapp"),
    path("about_us/", views.about, name="about"),
]
