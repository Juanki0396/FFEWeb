from django import forms

from ffeweb.choices import Provincia
from ffeweb.validators import validar_nif, validar_telefono

class RegistroBaseForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)
    first_name = forms.CharField(label="Nombre", max_length=64, required=True)
    last_name = forms.CharField(label="Apellidos", max_length=128, required=True)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cleaned_data

class RegistroConTelefonoForm(RegistroBaseForm):
    telefono = forms.CharField(label="Telefono",max_length=16, required=True, validators=[validar_telefono])

class RegistroAdminInstitutoForm(RegistroConTelefonoForm):
    pass

class RegistroTutorForm(RegistroConTelefonoForm):
    pass

class RegistroTutorEmpresaForm(RegistroConTelefonoForm):
    pass

class RegistroAlumnoForm(RegistroConTelefonoForm):
    nif = forms.CharField(label="NIF",max_length=9, min_length=9, required=True, validators=[validar_nif])
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", required=True)
    pais_nacimiento = forms.CharField(label="Pais de nacimiento", max_length=64, required=True)
    direccion = forms.CharField(label="Dirección", max_length=128, required=True)
    codigo_postal = forms.CharField(label="Código postal", max_length=16, required=True)
    municipio = forms.CharField(label="Municipio", max_length=64, required=True)
    provincia = forms.ChoiceField(choices=Provincia, label="Provincia", required=True)

