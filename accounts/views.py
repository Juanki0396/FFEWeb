from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.utils import timezone


from .models import Invitacion

# Create your views here.
class InvitationRegisterView(View):

    def _get_invitacion_or_404(self, token):
        inv = get_object_or_404(Invitacion,token=token)
        if inv.usado or inv.fecha_expiracion < timezone.now():
            return None

    def get(self, request, token):
        inv = self._get_invitacion_or_404(token)
        if inv is None:
            return Http404()
        return HttpResponse("Token Encontrado")

    def post(self, request, token):
        pass
