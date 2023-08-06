from rest_framework import viewsets, status, response, generics, permissions
from django.db.models import Q
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.shortcuts import get_object_or_404
from blog.serializers import *
from blog.utils import ActionBasedPermission


class ArticleCategoryViewSet(viewsets.ModelViewSet):
    '''This ViewSet class is for managing the CRUD operations on ArticleCategory model'''
    serializer_class = ArticleCategorySerializer
    queryset = ArticleCategory.objects.all()
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        '''
        if it found 'status' in 'query_params' then it will return categories list of the current status
        otherwise it will return only active categories list
        '''
        queryset = self.get_queryset().filter(status__exact=request.GET.get('status', None) or 'active')
        return response.Response(self.serializer_class(queryset, many=True).data, status=status.HTTP_200_OK)


class ArticleSubcategoryViewSet(viewsets.ModelViewSet):
    '''This ViewSet class is for managing the CRUD operations on ArticleSubcategory model'''
    serializer_classes = {
        'create': CreateArticleSubcategorySerializer,
        'list': ListArticleSubcategorySerializer,
        'retrieve': ListArticleSubcategorySerializer,
        'update': CreateArticleSubcategorySerializer
    }
    default_serializer_class = ListArticleSubcategorySerializer
    queryset = ArticleSubcategory.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def list(self, request, *args, **kwargs):
        '''
        if it found 'category_slug' and 'status' in 'query_params' then it will return the list of subcategories of this
        given category and the given status otherwise it will return the list of active subcategories
        '''
        queryset = self.get_queryset().filter(Q(category__slug__exact=request.GET.get('category_slug')) &
                                              Q(status__exact=request.GET.get('status', None) or 'active')) \
            if request.GET.get('category_slug', None) else self.get_queryset().filter(status__exact=request.GET.
                                                                                      get('status', None) or 'active')
        return response.Response(self.get_serializer_class()(queryset, many=True).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['category'].status != 'active': return response.Response(
            {'detail': 'Category is inactive.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        return response.Response(self.get_serializer_class()(get_object_or_404(ArticleSubcategory, slug=kwargs['slug']),
                                                             many=False).data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        query = get_object_or_404(ArticleSubcategory, slug=kwargs['slug'])
        serializer = self.get_serializer_class()(query, data=request.data, partial=True)
        serializer.is_valid()
        if 'category' in serializer.validated_data and serializer.validated_data['category'].status != 'active':
            return response.Response({'detail': 'Category is inactive'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class ArticleViewSet(viewsets.ModelViewSet):
    '''This ViewSet class is for managing the CRUD operations on Article model'''
    serializer_classes = {
        'create': CreateArticleSerializer,
        'list': ListArticleSerializer,
        'retrieve': ListArticleSerializer,
        'update': CreateArticleSerializer
    }
    default_serializer_class = ListArticleSerializer
    permission_classes = [permissions.AllowAny, ]
    queryset = Article.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def list(self, request, *args, **kwargs):
        '''
        1. if it found 'subcategory_slug' and 'status' then it will return all the articles of this given category and given status
        2. if it found only 'subcategory_slug' then it will return all the active articles of this given category
        3. if it found only 'status' then it will return all the articles of the given status
        4. if it does not found 'status' and 'subcategory_slug' then it will return all the active articles
        '''
        queryset = self.get_queryset().filter(Q(subcategory__slug=request.GET.get('subcategory_slug')) &
                                              Q(status__exact=request.GET.get('status', None) or 'active')) \
            if request.GET.get('subcategory_slug', None) \
            else self.get_queryset().filter(status__exact=request.GET.get('status', None) or 'active')
        return response.Response(self.get_serializer_class()(queryset, many=True).data,
                                 status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        payload = request.data.copy()
        if 'tags' not in payload:payload['tags'] = []
        serializer = self.get_serializer_class()(data=payload)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['subcategory'].status != 'active':
            return response.Response({'detail': 'Subcategory is inactive'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        return response.Response(self.get_serializer_class()(get_object_or_404(Article, slug=kwargs['slug']),
                                                             many=False).data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        query = get_object_or_404(Article, slug=kwargs['slug'])
        serializer = self.get_serializer_class()(query, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if 'subcategory' in serializer.validated_data and serializer.validated_data['subcategory'].status != 'active':
            return response.Response({'detail': 'Subcategory is inactive'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class RelatedArticlesListAPI(generics.GenericAPIView):
    '''This API will return related_articles, it accepts article slug in query params'''
    serializer_class = ListArticleSerializer
    queryset = Article.objects.all()

    def get(self, request, *args, **kwargs):
        if not request.GET.get('slug', None): return response.Response({'detail': 'Article slug is required in params'},
                                                                       status=status.HTTP_400_BAD_REQUEST)
        query = get_object_or_404(Article, slug=request.GET.get('slug'))
        queryset = query.tags.similar_objects()
        [queryset.remove(article) for article in queryset if article.status != 'active']
        serializer = self.serializer_class(queryset, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class ArticleLikeAndDislikeAPI(generics.GenericAPIView):
    '''
    This API is used to like and dislike on article
    '''
    serializer_class = LikeAndDislikeSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        payload = request.data.copy()
        payload['user'] = request.user.id
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.validated_data, status=status.HTTP_200_OK)


class ArticleCommentViewSet(viewsets.ModelViewSet):
    '''
    This API is for managing the CRUD operations on Comment model
    '''
    serializer_classes = {
        'list': ListCommentSerializer,
        'create': CreateCommentSerializer
    }
    default_serializer_class = ListCommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        permissions.IsAuthenticated: ['update', 'partial_update', 'destroy', 'create'],
        permissions.AllowAny: ['retrieve', 'list']
    }
    lookup_field = 'pk'

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def list(self, request, *args, **kwargs):
        '''
        It accepts 'article_id' in params and return all the active comments of the given article
        '''
        blog_id = request.GET.get('article_id', None)
        if not blog_id: return response.Response({'detail': 'article_id required in params.'},
                                                 status=status.HTTP_400_BAD_REQUEST)
        return response.Response(self.get_serializer_class()(get_object_or_404(Article, pk=int(blog_id)).comments.
                                                             filter(status__exact='active'), many=True).data,
                                 status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        payload = request.data.copy()
        payload['user'] = request.user.id
        serializer = self.get_serializer_class()(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        query = get_object_or_404(Comment, pk=kwargs['pk'])
        if query.user != request.user:
            return response.Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer_class()(query, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        query = get_object_or_404(Comment, pk=kwargs['pk'])
        if query.user != request.user:
            return response.Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        query.delete()
        return response.Response({'detail': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ArticleSearchAPI(generics.ListAPIView):
    '''This API is to search the articles'''
    serializer_class = ListArticleSerializer
    queryset = Article.objects.filter(status__exact='active')
    filter_backends = [filters.SearchFilter]
    search_fields = ['subcategory__title', 'subcategory__slug', 'title', 'author_name', 'author__first_name',
                     'author__last_name', 'author__username', 'author__email', 'keywords', 'seo_title', 'tags__name']


