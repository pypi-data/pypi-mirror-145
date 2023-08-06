from django.urls import path
from ucamwebauth.views import raven_login, raven_logout, raven_return

urlpatterns = [
    path('accounts/login/', raven_login, name='raven_login'),
    path('accounts/logout/', raven_logout, name='raven_logout'),
    path('raven_return/', raven_return, name='raven_return'),
]
