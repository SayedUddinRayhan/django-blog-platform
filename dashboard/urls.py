from django.urls import path
from .views import DashboardView, CategoriesView


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('categories/', CategoriesView.as_view(), name='categories'),
]
