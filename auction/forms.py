from django import forms
from django.contrib.auth.models import User

from .models import Lot_sub, UserProfile, LotRate, Winner

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = 'Enter the ' + field_name

class UserForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password')

class UserProfileForm(BaseForm):
    class Meta:
        model = UserProfile
        fields = ()

class LotForm(BaseForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Lot_sub
        fields = ('title', 'text', 'starting_price', 'end_date', 'image')

class RateForm(BaseForm):
    class Meta:
        model = LotRate
        fields = ('rate',)

class WinnerForm(BaseForm):
    class Meta:
        model = Winner
        fields = ()
