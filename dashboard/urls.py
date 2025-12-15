from django.urls import path
from .views import DashboardView, CategoriesView, BlogPostsView, AddCategoryView, AddBlogPostView


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('categories/add/', AddCategoryView.as_view(), name='add_category'),
    path('blogposts/', BlogPostsView.as_view(), name='blogposts'),
    path('blogposts/add/', AddBlogPostView.as_view(), name='add_blogpost'),
]
