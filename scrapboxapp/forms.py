from django import forms
from django.contrib.auth.models import User
from scrapboxapp.models import ScrapModel,UserProfileModel,BidsModel
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]

        widgets={
            "username":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter username"}),
            "email":forms.TextInput(attrs={"class":"form-control","placeholder":"name@example.com"}),
        }
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder':"Enter a password",
            })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'Placeholder':'Confirm Password',})
        
class SigninForm(forms.Form):
    username=forms.CharField(widget=(forms.TextInput(attrs={"class":"form-control","placeholder":"Enter username"})))
    password=forms.CharField(widget=(forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter password"})))

class ProductForm(forms.ModelForm):
    class Meta:
        model=ScrapModel
        fields=["name","price","category","location","condition","description","picture"]
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "price":forms.NumberInput(attrs={"class":"form-control"}),
            "category":forms.Select(attrs={"class":"form-control"}),
            "location":forms.TextInput(attrs={"class":"form-control"}),
            "condition":forms.Select(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control","rows":"4","wrap":"hard"}),
            "image":forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfileModel
        fields=["pic","first_name","last_name","contact"]

class BidForm(forms.ModelForm):
    class Meta:
        model=BidsModel
        fields=["amount"]
        widgets={
            "amount":forms.NumberInput(attrs={"class":"form-control"}),
        }





