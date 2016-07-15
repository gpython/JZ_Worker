#encoding:utf-8
from django.contrib import admin
import models

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('id', 'name')

class ArticleAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'author', 'hidden', 'publish_date', 'category')

class CommentAdmin(admin.ModelAdmin):
  list_display = ('id', 'article', 'user', 'comment', 'date')

class ThumbUpAdmin(admin.ModelAdmin):
  list_display = ('id', 'article', 'user', 'date')

class UserProfileAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'name')

class UserGroupAdmin(admin.ModelAdmin):
  list_display = ('id', 'name')

admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.ThumbUp, ThumbUpAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.UserGroup, UserGroupAdmin)
