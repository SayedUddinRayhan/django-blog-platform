from guardian.shortcuts import assign_perm, get_objects_for_user
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from blog.models import Category, BlogPost
from django.contrib.auth.models import User
from .forms import CategoryForm, BlogPostForm, DashboardAddUserForm, DashboardUserEditForm
from django.http import HttpResponseForbidden

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'total_categories': Category.objects.count(),
            'total_posts': BlogPost.objects.count(),
            'published_posts': BlogPost.objects.filter(status='published').count(),
        }

        if request.user.has_perm('auth.view_user'):
            context['total_users'] = User.objects.count()

        return render(request, 'dashboard/dashboard.html', context)
    
class CategoriesView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'blog.view_category'
    def get(self, request):
        # Context Processor theke categories niye aschi, tai ekhane ar lagbe na
        return render(request, 'dashboard/categories.html')

class AddCategoryView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'blog.add_category'
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

class EditCategoryView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'blog.change_category'
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=category)
       
        context = {
            'form': form,
            'category': category,
        }

        return render(request, 'dashboard/edit_category.html', context)
    
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        if not request.user.has_perm('blog.change_blogpost', blog_post):
            return HttpResponseForbidden()

        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
        
        context = {
            'form': form,
            'category': category,
        }
        return render(request, 'dashboard/edit_category.html', context)

class DeleteCategoryView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'blog.delete_category'
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect('categories')

class BlogPostsView(LoginRequiredMixin, View):
    def get(self, request):
        posts = get_objects_for_user(request.user, 'blog.view_blogpost', BlogPost, accept_global_perms=True)
        context = {
            'posts': posts,
        }
        return render(request, 'dashboard/blogposts.html', context)


class BlogPostsView(LoginRequiredMixin, View):
    def get(self, request):
        url_name = request.resolver_match.url_name

        # My Blogs → Author / Editor
        if url_name == 'my_blogposts':
            if not request.user.has_perm('blog.add_blogpost'):
                return HttpResponseForbidden()

            posts = BlogPost.objects.filter(author=request.user)

        # All Blogs → Editor / Admin
        else:
            if not request.user.has_perm('blog.view_blogpost'):
                return HttpResponseForbidden()

            posts = get_objects_for_user(request.user, 'blog.view_blogpost', BlogPost, accept_global_perms=True)

        context = {
            'posts': posts,
        }
        return render(request, 'dashboard/blogposts.html', context)
    
      

     



class AddBlogPostView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'blog.add_blogpost'
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

            assign_perm('blog.view_blogpost', request.user, blog_post)
            assign_perm('blog.change_blogpost', request.user, blog_post)
            assign_perm('blog.delete_blogpost', request.user, blog_post)


            return redirect('blogposts')
        
        context = {
            'form': form,
        }
        return render(request, 'dashboard/add_blogpost.html', context)
    
class EditBlogPostView(LoginRequiredMixin, View):
    def get(self, request, pk):
        blog_post = get_object_or_404(get_objects_for_user(request.user, 'blog.change_blogpost', BlogPost, accept_global_perms=True), pk=pk)

        form = BlogPostForm(instance=blog_post)
       
        context = {
            'form': form,
            'blog_post': blog_post,
        }

        return render(request, 'dashboard/edit_blogpost.html', context)
    
    def post(self, request, pk):
        blog_post = get_object_or_404(get_objects_for_user(request.user, 'blog.change_blogpost', BlogPost, accept_global_perms=True), pk=pk)

        form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('blogposts')
        
        context = {
            'form': form,
            'blog_post': blog_post,
        }
        return render(request, 'dashboard/edit_blogpost.html', context)
    
class DeleteBlogPostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        blog_post = get_object_or_404(get_objects_for_user(request.user, 'blog.delete_blogpost', BlogPost, accept_global_perms=True), pk=pk)
        blog_post.delete()
        return redirect('blogposts')


class UserManagementView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'auth.view_user'
    def get(self, request):
        users = User.objects.all()

        context = {
            'users': users,
        }
        return render(request, 'dashboard/user_management.html', context)
    
class AddUserView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'auth.add_user'
    def get(self, request):
        form = DashboardAddUserForm()
       
        context = {
            'form': form,
        }

        return render(request, 'dashboard/add_user.html', context)
    
    def post(self, request):
        form = DashboardAddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_management')
        
        context = {
            'form': form,
        }
        return render(request, 'dashboard/add_user.html', context)


class EditUserView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'auth.change_user'
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = DashboardUserEditForm(instance=user)
       
        context = {
            'form': form,
            'user_obj': user,
        }

        return render(request, 'dashboard/edit_user.html', context)
    
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = DashboardUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_management')
        
        context = {
            'form': form,
            'user_obj': user,
        }
        return render(request, 'dashboard/edit_user.html', context)
    
class DeleteUserView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'auth.delete_user'
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect('user_management')