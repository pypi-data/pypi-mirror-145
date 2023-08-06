from rest_framework import serializers, exceptions
from taggit.models import Tag
from taggit.serializers import TagListSerializerField, TaggitSerializer
from django.shortcuts import get_object_or_404
from blog.models import ArticleCategory, ArticleSubcategory, Article, User, Comment


class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = '__all__'


class CreateArticleSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleSubcategory
        fields = '__all__'


class ListArticleSubcategorySerializer(serializers.ModelSerializer):
    '''This serializer is to return the proper data of list and retrieve apis'''
    category = ArticleCategorySerializer(many=False)

    class Meta:
        model = ArticleSubcategory
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']


class CreateArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Article
        fields = '__all__'


class ListArticleSerializer(serializers.ModelSerializer):
    subcategory = ListArticleSubcategorySerializer(many=False)
    author = serializers.SerializerMethodField('get_author_full_name')
    tags = TagSerializer(many=True)
    like = serializers.SerializerMethodField('get_total_likes')
    comments = serializers.SerializerMethodField('get_total_comments')

    def get_total_likes(self, instance):
        return instance.like.all().count()

    def get_total_comments(self, instance):
        return instance.comments.all().count()

    def get_author_full_name(self, instance):
        try:
            return f'{self.author.first_name} {self.author.last_name}'
        except:
            return None

    class Meta:
        model = Article
        fields = '__all__'


class LikeAndDislikeSerializer(serializers.Serializer):
    '''This Serializer Class is for like and dislike on articles'''
    user = serializers.IntegerField()
    article = serializers.IntegerField()

    def validate(self, attrs):
        article = get_object_or_404(Article, id=attrs['article'])
        article.like.remove(attrs['user']) if article.like.filter(pk=attrs['user']).last() else article.like.add(
            attrs['user'])
        return {'likes': article.total_likes()}


class CreateCommentSerializer(serializers.Serializer):
    article = serializers.IntegerField()
    user = serializers.IntegerField()
    body = serializers.CharField()

    def validate(self, attrs):
        article = get_object_or_404(Article, id=attrs['article'])
        if article.allow_comments is False:
            raise exceptions.PermissionDenied('Comments are not allowed for this article')
        response_data = {
            'article': article,
            'user': User.objects.get(pk=attrs['user']),
            'body': attrs['body']
        }
        return response_data

    def create(self, validated_data):
        new_comment = Comment.objects.create(user=validated_data['user'], body=validated_data['body'])
        validated_data['article'].comments.add(new_comment)
        res = {
            'article': validated_data['article'].id,
            'user': validated_data['user'].id,
            'body': validated_data['body']
        }
        return res


class ListCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Comment
        fields = '__all__'

