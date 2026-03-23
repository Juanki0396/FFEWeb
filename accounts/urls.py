from django.urls import path
from .views import InvitationRegisterView

urlpatterns = [
    path('invitacion/<str:token>/', InvitationRegisterView.as_view(), name='invitacion_registro'),
]
