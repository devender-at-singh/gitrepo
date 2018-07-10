from django.contrib import admin
from django.conf import settings
# Register your models here.
from .models import Post, Comment,PostImage,Profile, Contact


# class PostImageInline(admin.TabularInline):
#     model = PostImage
class ImageAdmin(admin.ModelAdmin):
    pass
    # = ('image','description','title')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish','status')
    list_filter = ('status', 'created', 'publish', 'author')


    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    # inlines = PostImageInline,
    # class Media:
    #     js = (
    #         settings.STATIC_URL + 'js/tiny_mce/tiny_mce.js',
    #         settings.STATIC_URL + 'js/textareas.js',
    #     )

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created' ,'active')
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','date_of_birth','about_author','photo')
    # pass
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone','query')


admin.site.register(Post,PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostImage,ImageAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Contact,ContactAdmin)