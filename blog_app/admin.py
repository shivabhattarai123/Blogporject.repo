from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = "Blog Admin"
admin.site.site_title = "Blog Admin Portal"
admin.site.index_title = "Welcome to  Blog Portal"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    list_filter = ('name',)
    search_fields = ('name',)
admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','content','author','category','created_at',)
    list_filter = ('title','created_at',)
    serach_fields = ('title',)
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','post','content','created_at',)
    list_filter = ('content',)
    list_fields = ('post',)

admin.site.register(Comment, CommentAdmin)


