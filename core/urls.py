from django.urls import path
from .views import CheckStatusView, CheckCurrentUserView

urlpatterns = [
    path('', CheckStatusView.as_view(), name='check-status'),
    path('current-user/', CheckCurrentUserView.as_view(), name='check-current-user'),
]