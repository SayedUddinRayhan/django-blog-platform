from django import forms
from blog.models import Category, BlogPost
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'category', 'featured_image', 'short_description', 'blog_body', 'status', 'is_featured']


class DashboardAddUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_staff = forms.BooleanField(required=False)
    is_active = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = User
        # fields = ['username', 'email','password1','password2','is_active','is_staff']
        # user creation form use korle password1 and password2 automatically add hoye jay
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']


class DashboardUserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'groups', 'user_permissions']
