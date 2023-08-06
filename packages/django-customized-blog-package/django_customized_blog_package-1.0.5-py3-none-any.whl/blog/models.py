from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from blog.helpers import slug_generator


User = get_user_model()


class AbstractCommonFields(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ArticleCategory(AbstractCommonFields):
    title = models.CharField(max_length=100, unique=True, primary_key=False, verbose_name='category name',
                             help_text='Category name length should be in 100 characters')
    slug = models.SlugField(max_length=255, unique=True, primary_key=False, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['-id', ]


@receiver(pre_save, sender=ArticleCategory)
def _pre_save_receiver(sender, instance, *args, **kwargs):
    try:
        old_value = sender.objects.get(id=instance.id).title
        if old_value != instance.title:instance.slug = slug_generator(instance)
    except:
        instance.slug = slug_generator(instance)


class ArticleSubcategory(AbstractCommonFields):
    category = models.ForeignKey(ArticleCategory, on_delete=models.RESTRICT, help_text='Only active categories will be '
                                                                                       'displayed here')
    title = models.CharField(max_length=100, unique=True, primary_key=False, verbose_name='subcategory name',
                             help_text='Subcategory name length should be in 100 characters')
    slug = models.SlugField(max_length=255, blank=True, null=True, unique=True, primary_key=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'
        ordering = ['-id', ]


@receiver(pre_save, sender=ArticleSubcategory)
def _pre_save_receiver(sender, instance, *args, **kwargs):
    try:
        old_value = sender.objects.get(id=instance.id).title
        if old_value != instance.title: instance.slug = slug_generator(instance)
    except:
        instance.slug = slug_generator(instance)


class Article(AbstractCommonFields):
    subcategory = models.ForeignKey(ArticleSubcategory, on_delete=models.RESTRICT, help_text='Only active subcategories'
                                                                                             ' will displayed here')
    title = models.CharField(max_length=200, help_text='Blog title length should be within 200')
    slug = models.SlugField(max_length=255, blank=True, null=True, unique=True, primary_key=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', blank=True,
                               null=True)
    author_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='Custom author name',
                                   help_text='Ex. John Doe')
    introduction = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    body = RichTextUploadingField()
    thumbnail = models.ImageField(upload_to='articles/thumbnails/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='articles/cover-images/', blank=True, null=True)
    image_alt_tag = models.CharField(max_length=50, blank=True, null=True)
    image_caption = models.CharField(max_length=50, blank=True, null=True)
    keywords = models.CharField(max_length=255, help_text='Keywords must be separated by comma(,)')
    tags = TaggableManager(blank=True)
    seo_title = models.CharField(max_length=200, blank=True, null=True)
    seo_introduction = models.TextField(blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.CharField(max_length=255, blank=True, null=True,
                                    help_text='SEO-Keywords must be separated by comma(,)')
    display_date = models.CharField(max_length=50, blank=True, null=True, verbose_name='Custom publish date',
                                    help_text='Ex. 12th March, 2022')
    like = models.ManyToManyField(User, blank=True, null=True, related_name='like')
    comments = models.ManyToManyField('Comment', blank=True, null=True, related_name='comment')
    allow_comments = models.BooleanField(default=False)
    change_status_on = models.DateTimeField(blank=True, null=True)

    def total_likes(self):
        return self.like.all().count()

    def total_views(self):
        return self.view.all().count()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.seo_title = self.seo_title or self.title
        self.introduction = self.seo_introduction or self.introduction
        self.seo_description = self.seo_description or self.description
        self.seo_keywords = self.seo_keywords or self.keywords
        super(Article, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-created_on', ]


@receiver(pre_save, sender=Article)
def _pre_save_receiver(sender, instance, *args, **kwargs):
    try:
        old_value = sender.objects.get(id=instance.id).title
        if old_value != instance.title: instance.slug = slug_generator(instance)
    except:
        instance.slug = slug_generator(instance)


@receiver(post_save, sender=Article)
def _post_save_receiver(sender, instance, *args, **kwargs):
    from task_app.helpers import create_or_update_task
    if instance.change_status_on:
        create_or_update_task(instance)


class Comment(AbstractCommonFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return f'Comment by: {self.user.first_name} {self.user.last_name}, body: {self.body}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-id', ]


