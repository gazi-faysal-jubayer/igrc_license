from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup_superuser, name='signup_superuser'),
    path('login/', login_superuser, name='login_superuser'),
    path('create-agency/', CreateAgencyView.as_view(), name='create_agency'),
    path('agency-login/', AgencyLoginView.as_view(), name='agency-login'),
    path('csrf-token/', csrf_token_view, name='csrf_token'),

]
