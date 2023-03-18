from django.contrib import admin

from .models import Post, Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created', 'date_updated')
    list_filter = ('date_created', 'date_updated')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
# admin.site.register(Like)


'''
class CommentInline(admin.TabularInline):
    model = Comment
    # extra = 0

class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]
'''