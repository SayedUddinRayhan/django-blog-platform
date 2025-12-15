from django.urls import path
from .views import (
    DashboardView, 
    CategoriesView, 
    BlogPostsView, 
    AddCategoryView, 
    EditCategoryView, 
    DeleteCategoryView, 
    AddBlogPostView, 
    EditBlogPostView, 
    DeleteBlogPostView,
    UserManagementView,
    AddUserView,
    EditUserView,
    DeleteUserView
    )


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('categories/add/', AddCategoryView.as_view(), name='add_category'),
    path('categories/edit/<int:pk>/', EditCategoryView.as_view(), name='edit_category'),
    path('categories/delete/<int:pk>/', DeleteCategoryView.as_view(), name='delete_category'),
    path('blogposts/', BlogPostsView.as_view(), name='blogposts'),
    path('blogposts/add/', AddBlogPostView.as_view(), name='add_blogpost'),
    path('blogposts/edit/<int:pk>/', EditBlogPostView.as_view(), name='edit_blogpost'),
    path('blogposts/delete/<int:pk>/', DeleteBlogPostView.as_view(), name='delete_blogpost'),

    path('users/', UserManagementView.as_view(), name='user_management'),
    path('users/add/', AddUserView.as_view(), name='add_user'),
    path('users/edit/<int:pk>/', EditUserView.as_view(), name='edit_user'),
    path('users/delete/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),
]
