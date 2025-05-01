from django.urls import path
from ForensicApp import views
urlpatterns = [
    path('login',views.login),
    path('register', views.register),
    path('regaction',views.regaction),
    path('home',views.home),
    path('logaction',views.logaction),
    path('ViewCrime',views.ViewCrime),
    path('GenerateReport', views.GenerateReport),
    path('AddFReportAction', views.AddFReportAction),
    path('ViewForensicReport', views.ViewForensicReport),
]
