from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Category, BlogPost
from django.contrib.auth.models import User
from .forms import CategoryForm, BlogPostForm


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        context = {
            'total_categories': Category.objects.count(),
            'total_posts': BlogPost.objects.count(),
            'published_posts': BlogPost.objects.filter(status='published').count(),
            'is_manager': user.groups.filter(name='Manager').exists(),
            'is_editor': user.groups.filter(name='Editor').exists(),
        }

        if context['is_manager']:
            context['total_users'] = User.objects.count()

        return render(request, 'dashboard/dashboard.html', context)
    
class CategoriesView(LoginRequiredMixin, View):
    def get(self, request):
        # Context Processor theke categories niye aschi, tai ekhane ar lagbe na
        return render(request, 'dashboard/categories.html')

class AddCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        form = CategoryForm()
       
        context = {
            'form': form,
        }

        return render(request, 'dashboard/add_category.html', context)
    
    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
        
        context = {
            'form': form,
        }
        return render(request, 'dashboard/add_category.html', context)

class BlogPostsView(LoginRequiredMixin, View):
    def get(self, request):
        posts = BlogPost.objects.all()
        context = {
            'posts': posts,
        }
        return render(request, 'dashboard/blogposts.html', context)
    
class AddBlogPostView(LoginRequiredMixin, View):
    def get(self, request):
        form = BlogPostForm()
       
        context = {
            'form': form,
        }

        return render(request, 'dashboard/add_blogpost.html', context)
    
    def post(self, request):
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False) 
            blog_post.author = request.user      
            blog_post.save()                   
            return redirect('blogposts')
        
        context = {
            'form': form,
        }
        return render(request, 'dashboard/add_blogpost.html', context)