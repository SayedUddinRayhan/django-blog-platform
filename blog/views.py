from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Category, BlogPost, About, FollowUs, Comment
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import CommentForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(View):
    def get(self, request):
        # I have created a context processor to get all categories
        # categoriesQ = Category.objects.all()
        featured_postsQ = BlogPost.objects.filter(is_featured=True, status='published').order_by('-updated_at')
        posts = BlogPost.objects.filter(is_featured=False, status='published').order_by('-updated_at')
        about_infoQ = About.objects.first()
        follow_usQ = FollowUs.objects.all()

        paginator = Paginator(posts, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            # 'categories': categoriesQ,
            'featured_posts': featured_postsQ,
            'posts': posts,
            'about_info': about_infoQ,
            'follow_us': follow_usQ,
            'page_obj': page_obj,
        }

        return render(request, 'home.html', context)
    

class CategoryView(View):
    def get(self, request, slug):

        # category_id = Category.objects.get(id=category_id)
        # category = get_object_or_404(Category, id=category_id)

        # try:
        #     category = Category.objects.get(id=category_id)
        # except Category.DoesNotExist:
        #     return redirect('home')
        
        category = get_object_or_404(Category, slug=slug)

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
        form = CommentForm()
        comments = post.comments.filter(active=True, parent__isnull=True).select_related('author').prefetch_related('replies')
        total_comments = 0
        for comment in comments:
            total_comments += 1
            total_comments += comment.replies.filter(active=True).count()

        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'total_comments': total_comments
        }
        return render(request, 'blogpost_detail.html', context)
    
    def post(self, request, slug):
        post = get_object_or_404(BlogPost, slug=slug, status='published')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog_post = post
            comment.author = request.user

            # Repies
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)

            comment.save()
            messages.success(request, 'Comment added successfully.')

            return redirect('blogpost_detail', slug=post.slug)
        
        comments = post.comments.filter(active=True, parent__isnull=True)
        context = {
            'post': post,
            'form': form,
            'comments': comments
        }
        return render(request, 'blogpost_detail.html', context)

        
    
class SearchView(View):
    def get(self, request):
        query = request.GET.get('keyword', '')
        postsQ = BlogPost.objects.none()

        if query:
            postsQ = BlogPost.objects.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(blog_body__icontains=query),
            status='published'
         ).order_by('-updated_at')
            
        
        # Pagination
        paginator = Paginator(postsQ, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'search_query': query,
            'page_obj': page_obj
        }
        return render(request, 'search_results.html', context)
    

class EditCommentView(LoginRequiredMixin, View):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if comment.author != request.user and not request.user.is_staff:
            return redirect('blogpost_detail', slug=comment.blog_post.slug)

        form = CommentForm(instance=comment)

        context = {
            'form': form,
            'comment': comment
        }

        return render(request, 'edit_comment.html', context)

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if comment.author != request.user and not request.user.is_staff:
            return redirect('blogpost_detail', slug=comment.blog_post.slug)

        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blogpost_detail', slug=comment.blog_post.slug)
        
        context = {
            'form': form,
            'comment': comment
        }

        return render(request, 'edit_comment.html', context)
    
class DeleteCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if comment.author != request.user and not request.user.is_staff:
            messages.error(request, 'You do not have permission to remove this comment.')
            return redirect('blogpost_detail', slug=comment.blog_post.slug)

        comment.active = False
        comment.save()
        messages.success(request, 'Comment removed successfully.')
        return redirect('blogpost_detail', slug=comment.blog_post.slug)

