from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Contraseña' , widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña' , widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username' , 'first_name' , 'last_name','email','password1' , 'password2']
        help_texts ={k:"" for k in fields}
    
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-input mt-2'
            
            self.fields['username'].widget.attrs['class'] = 'form-input mt-2  w-full rounded-full pl-4 '
            self.fields['first_name'].widget.attrs['class'] = 'form-input  w-full mt-2  rounded-full pl-4'
            self.fields['last_name'].widget.attrs['class'] = 'form-input mt-2  w-full rounded-full pl-4'
            self.fields['email'].widget.attrs['class'] = 'form-input mt-2  w-full rounded-full pl-4'
            self.fields['password1'].widget.attrs['class'] = 'form-input mt-2  w-full rounded-full pl-4'
            self.fields['password2'].widget.attrs['class'] = 'form-input mt-2 flex w-full rounded-full pl-4'
            
            
            


