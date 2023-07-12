from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'signapp'

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='signapp/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='signapp/logout.html'),
         name='logout'),
]
