from django.urls import path
from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login3'),
]
