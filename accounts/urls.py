from django.conf.urls import url
from accounts import views

urlpattern = [
    url(r'^send_email$', views.send_login_email, name='send_login_email'),
]