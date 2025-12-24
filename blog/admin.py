from guardian.admin import GuardedModelAdmin
from django.contrib import admin
from .models import Category, BlogPost, About, FollowUs


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# For BlogPost Slug field prepopulation
class BlogPostAdmin(GuardedModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_featured', 'updated_at',)
    search_fields = ('title', 'category__name', 'author__username', 'status',)
    list_editable = ('is_featured',)


    # Superuser chara onno user jodi admin theke blog post add or edit kore tahole author field ta disabled thakbe
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if not request.user.is_superuser:
            # Author cannot change author field
            form.base_fields['author'].disabled = True

        return form

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user  # enforce ownership
        obj.save()


# -------- SINGLETON ABOUT ADMIN --------
class AboutAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if About.objects.exists():
            return False
        return super().has_add_permission(request)

    list_display = ('about_heading', 'updated_at')


admin.site.register(Category, CategoryAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(FollowUs)