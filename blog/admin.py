from django.contrib import admin
from .models import Category, BlogPost


# For BlogPost Slug field prepopulation
class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_featured', 'updated_at',)
    search_fields = ('title', 'category__name', 'author__username', 'status',)
    list_editable = ('is_featured',)

admin.site.register(Category)
admin.site.register(BlogPost, BlogPostAdmin)
