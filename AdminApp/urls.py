


from django.urls import path
from AdminApp import views
urlpatterns = [
    path('',views.index),
    path('login',views.login),
    path('logaction',views.logaction),
    path('home',views.home),
    path('ViewForensic',views.ViewForensic),
    path('Accept',views.Accept),
    path('AddPolice',views.AddPolice),
    path('AddPction',views.AddPction),
    path('ViewPolice',views.ViewPolice),

]
