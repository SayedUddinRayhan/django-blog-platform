from django.urls import path
from .views import HomeView, CategoryView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category_view')
]
