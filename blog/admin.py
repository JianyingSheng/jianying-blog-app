# blog/admin.py

from django.contrib import admin
from . import models

##################################
class CommentInline(admin.TabularInline):
    model = models.Comment
##################################

class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]
    list_display = (
        'title',
        'author',
        'created',
        'updated',
    )
    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )
    prepopulated_fields = {'slug': ('title',)}
    list_filter = (
        'status',
    )
admin.site.register(models.Post,PostAdmin)

@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created', 'approved')
    list_filter = ('approved', 'created')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
