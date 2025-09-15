from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(
                choices=[(5, "⭐⭐⭐⭐⭐ - Excellent"),
                         (4, "⭐⭐⭐⭐ - Good"),
                         (3, "⭐⭐⭐ - Average"),
                         (2, "⭐⭐ - Poor"),
                         (1, "⭐ - Very Bad")],
                attrs={"class": "form-select"}
            ),
            "comment": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Write your review..."}
            ),
        }