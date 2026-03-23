from django.forms import ModelForm

from .models import Instituto

class InstitutoForm(ModelForm):
    class Meta:
        model = Instituto
        exclude = ["ciclos"]
