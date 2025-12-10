from django.shortcuts import render
from django.views import View
from .models import Category, BlogPost

class HomeView(View):
    def get(self, request):

        categoriesQ = Category.objects.all()
        featured_postsQ = BlogPost.objects.filter(is_featured=True, status='published').order_by('-updated_at')
        posts = BlogPost.objects.filter(is_featured=False, status='published').order_by('-updated_at')
        context = {
            'categories': categoriesQ,
            'featured_posts': featured_postsQ,
            'posts': posts,
        }

        return render(request, 'home.html', context)
    

class CategoryView(View):
    def get(self, request, category_id):
        postsQ = BlogPost.objects.filter(status='published', category=category_id)
        category_id = Category.objects.get(id=category_id)
        categoriesQ = Category.objects.all()
        context = {
            'posts': postsQ,
            'category': category_id,
            'categories': categoriesQ,
        }
        return render(request, 'category.html', context)