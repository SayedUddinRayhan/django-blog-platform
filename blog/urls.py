from django.urls import path
from .views import HomeView, CategoryView, BlogPostDetailView, SearchView, EditCommentView, DeleteCommentView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category_view'),
    path('blog/<slug:slug>/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('search/', SearchView.as_view(), name='search'),
    path('comment/edit/<int:pk>/', EditCommentView.as_view(), name='edit_comment'),
    path('comment/delete/<int:pk>/', DeleteCommentView.as_view(), name='delete_comment'),


]
