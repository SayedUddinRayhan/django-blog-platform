from django.contrib import admin
from .models import Category, BlogPost, About, FollowUs


# For BlogPost Slug field prepopulation
class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_featured', 'updated_at',)
    search_fields = ('title', 'category__name', 'author__username', 'status',)
    list_editable = ('is_featured',)


# -------- SINGLETON ABOUT ADMIN --------
class AboutAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if About.objects.exists():
            return False
        return super().has_add_permission(request)

    list_display = ('about_heading', 'updated_at')


admin.site.register(Category)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(FollowUs)