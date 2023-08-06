from django.contrib import admin
from blog.models import ArticleCategory, ArticleSubcategory, Article, Comment


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'slug', 'status', 'created_on', 'updated_on']
    readonly_fields = ['id', 'created_on', 'updated_on']
    search_fields = ['title', 'slug', 'id']
    search_help_text = ['Search by category name, slug and ID']
    list_display_links = ['title']
    list_per_page = 20


@admin.register(ArticleSubcategory)
class ArticleSubcategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'slug', 'category', 'status', 'created_on', 'updated_on']
    readonly_fields = ['id', 'created_on', 'updated_on']
    search_fields = ['title', 'slug', 'id']
    search_help_text = ['Search by subcategory name, slug and ID']
    list_display_links = ['title']
    list_per_page = 20
    list_filter = ['category']

    def get_form(self, request, obj=None, **kwargs):
        '''Override get_form method to get only active categories'''
        form = super(ArticleSubcategoryAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['category'].queryset = ArticleCategory.objects.filter(status__exact='active')
        return form


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'status', 'created_on', 'updated_on', 'change_status_on']
    readonly_fields = ['id', 'created_on', 'updated_on']
    search_fields = ['title', 'slug', 'id', 'seo_title', 'keywords']
    search_help_text = ['Search by category name, slug, ID, seo-title, keywords']
    list_display_links = ['title']
    list_per_page = 50

    def get_form(self, request, obj=None, **kwargs):
        '''Override get_form method to get only active subcategories'''
        form = super(ArticleAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['subcategory'].queryset = ArticleSubcategory.objects.filter(status__exact='active')
        return form


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'body', 'user', 'created_on', 'updated_on']

