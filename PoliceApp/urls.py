from django.urls import path
from PoliceApp import views
urlpatterns = [
    path('login',views.login),
    path('logaction', views.logaction),
    path('home', views.home),
    path('AddCrimeDetails',views.AddCrimeDetails),
    path('AddCrimeAction',views.AddCrimeAction),
    path('ViewCrime',views.ViewCrime),
    path('ViewForensicReport', views.ViewForensicReport),
]
