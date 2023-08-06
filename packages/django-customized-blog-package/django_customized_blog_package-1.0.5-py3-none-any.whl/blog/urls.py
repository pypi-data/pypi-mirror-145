from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import *

router = DefaultRouter()
router.register('categories', ArticleCategoryViewSet, basename='article_category')
router.register('subcategories', ArticleSubcategoryViewSet, basename='article_subcategory')
router.register('article', ArticleViewSet, basename='article')
router.register('comments', ArticleCommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('related-articles', RelatedArticlesListAPI.as_view(), name='related_articles'),
    path('like-and-dislike/', ArticleLikeAndDislikeAPI.as_view(), name='like_and_dislike'),
    path('search', ArticleSearchAPI.as_view(), name='search'),
]

