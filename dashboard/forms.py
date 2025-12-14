from django import forms
from blog.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter category name',
                    'autocomplete': 'off',
                }
            ),
        }
        labels = {
            'name': 'Category Name',
        }
