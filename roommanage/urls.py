from django.urls import path
from . import views

urlpatterns = [
path("", views.Index.as_view(),name="index"),
path("login",views.LoginPage.as_view(),name='login'),
path("dashboard",views.Dashboard.as_view(),name='dashboard'),
path("modal",views.Bookreason.as_view(),name="modal"),

]