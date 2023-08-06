from django.test import SimpleTestCase
from django.urls import resolve, reverse
from blog.views import *


class TestUrls(SimpleTestCase):

    def test_related_articles_is_resolved(self):
        url = reverse('related_articles')
        self.assertEquals(resolve(url).func.view_class, RelatedArticlesListAPI)




