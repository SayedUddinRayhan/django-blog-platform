from django.urls import path
from .views import DashboardView, CategoriesView, BlogPostsView, AddCategoryView, EditCategoryView, DeleteCategoryView, AddBlogPostView


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('categories/add/', AddCategoryView.as_view(), name='add_category'),
    path('categories/edit/<int:pk>/', EditCategoryView.as_view(), name='edit_category'),
    path('categories/delete/<int:pk>/', DeleteCategoryView.as_view(), name='delete_category'),
    path('blogposts/', BlogPostsView.as_view(), name='blogposts'),
    path('blogposts/add/', AddBlogPostView.as_view(), name='add_blogpost'),
]
