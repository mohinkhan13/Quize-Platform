from django.urls import path
from .views import *
urlpatterns = [

    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('setting/', setting, name='setting'),
    path('profile/', profile, name='profile'),
    path('change-password/', change_password, name='change-password'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('verify-otp/', verify_otp, name='verify-otp'),
    path('new-password/', new_password, name='new-password'),
    path('my-all-exams/', my_all_exams, name='my-all-exams'),
    path('create-exam/', create_exam, name='create-exam'),
]