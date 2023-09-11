from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserCreateForm(UserCreationForm):
    email= forms.EmailField(max_length=45,label="Correo Electronico", required=True)
    name= forms.CharField(max_length=45,label="Nombre", required=True)
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email','name','password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update(
                                      {'class': 'form-control'})
        