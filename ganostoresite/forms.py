from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Program, Comment, Complaint

User = get_user_model()

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'avatar', 'password1', 'password2')

class ProgramUploadForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ('title', 'description', 'category', 'genre', 'program_file', 'image')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('content',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'avatar')

class PasswordResetForm(forms.Form):
    email = forms.EmailField(max_length=254, help_text='Введіть адресу електронної пошти, повязану з вашим акаунтом.')
