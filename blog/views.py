from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Category, BlogPost, About, FollowUs

class HomeView(View):
    def get(self, request):
        # I have created a context processor to get all categories
        # categoriesQ = Category.objects.all()
        featured_postsQ = BlogPost.objects.filter(is_featured=True, status='published').order_by('-updated_at')
        posts = BlogPost.objects.filter(is_featured=False, status='published').order_by('-updated_at')
        about_infoQ = About.objects.first()
        follow_usQ = FollowUs.objects.all()
        context = {
            # 'categories': categoriesQ,
            'featured_posts': featured_postsQ,
            'posts': posts,
            'about_info': about_infoQ,
            'follow_us': follow_usQ,
        }

        return render(request, 'home.html', context)
    

class CategoryView(View):
    def get(self, request, category_id):

        # category_id = Category.objects.get(id=category_id)
        # category = get_object_or_404(Category, id=category_id)

        # try:
        #     category = Category.objects.get(id=category_id)
        # except Category.DoesNotExist:
        #     return redirect('home')
        
        category = get_object_or_404(Category, id=category_id)

        # I have created a context processor to get all categories
        # categoriesQ = Category.objects.all()

        postsQ = BlogPost.objects.filter(status='published', category=category).select_related('category').order_by('-updated_at') 
       
        context = {
            'posts': postsQ,
            'category': category,
            # 'categories': categoriesQ,
        }
        return render(request, 'category.html', context)
    
class BlogPostDetailView(View):
    def get(self, request, slug):
        post = get_object_or_404(BlogPost, slug=slug, status='published')

        context = {
            'post': post,
        }
        return render(request, 'blogpost_detail.html', context)