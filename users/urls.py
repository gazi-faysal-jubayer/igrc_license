from django.urls import path
from .views import signup_superuser, login_superuser, CreateAgencyView

urlpatterns = [
    path('signup/', signup_superuser, name='signup_superuser'),
    path('login/', login_superuser, name='login_superuser'),
    path('create-agency/', CreateAgencyView.as_view(), name='create_agency'),
]
