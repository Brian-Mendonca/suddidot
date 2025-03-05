from django.contrib import admin
from django import forms
from .models import Category, NewsArticle, Comment
from tinymce.widgets import TinyMCE
from django.utils.translation import gettext_lazy

admin.site.site_header = gettext_lazy("Suddidot News Admin")
admin.site.site_title = gettext_lazy("Suddidot Admin Portal")
admin.site.index_title = gettext_lazy("Welcome to the Suddidot News Management")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class NewsArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = NewsArticle
        fields = '__all__'

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  
    readonly_fields = ('created_at',)

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    form = NewsArticleAdminForm
    list_display = ('title', 'display_categories', 'is_trending', 'published_at')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_trending', 'categories')
    search_fields = ('title', 'content')
    filter_horizontal = ('categories',)
    inlines = [CommentInline    ]

    def display_categories(self, obj):
        return ", ".join(category.name for category in obj.categories.all())
    
    display_categories.short_description = "Categories"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'news_article', 'created_at')
    search_fields = ('name', 'message')