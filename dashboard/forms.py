from django import forms
from blog.models import Category, BlogPost


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

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'category', 'featured_image', 'short_description', 'blog_body', 'status', 'is_featured']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter blog post title',
                    'autocomplete': 'off',
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'featured_image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control-file',
                }
            ),
            'short_description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter a short description',
                    'rows': 3,
                }
            ),
            'blog_body': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter the blog content',
                    'rows': 10,
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'is_featured': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        }