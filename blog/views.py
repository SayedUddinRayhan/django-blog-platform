from django.shortcuts import render
from django.views import View
from .models import Category, BlogPost

class HomeView(View):
    def get(self, request):

        categoriesQ = Category.objects.all()
        featured_postsQ = BlogPost.objects.filter(is_featured=True, status='published').order_by('-updated_at')
        posts = BlogPost.objects.filter(is_featured=False, status='published').order_by('-updated_at')
        context = {
            'categories': categoriesQ if categoriesQ.exists() else None,
            'featured_posts': featured_postsQ if featured_postsQ.exists() else None,
            'posts': posts if posts.exists() else None,
        }

        return render(request, 'home.html', context)