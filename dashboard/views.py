from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Category, BlogPost
from django.contrib.auth.models import User

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
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'dashboard/categories.html', context)