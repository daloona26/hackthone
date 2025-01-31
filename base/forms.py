from django.forms import ModelForm
from .models import Submission, User
from django.contrib.auth.forms import UserCreationForm  

class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = '__all__'

class CustomCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password1', 'password2']