# Django
from django.test import TestCase
from django.utils.text import slugify

# Project
from blog.models import PostModel

class PostModelTestCase(TestCase):
    def setUp(self):
        PostModel.objects.create(
            title="Hola mundo test",
            slug="hola-mundo-test",
            )
    def create_post(self, title="Prueba 1"):
        return PostModel.objects.create(title=title)

    def test_postmodel_title(self):
        obj = PostModel.objects.get(slug="hola-mundo-test")
        self.assertEqual(obj.title, 'Hola mundo test')
        self.assertTrue(obj.content != '')
        print("test model title")
    
    def test_postsmodel_slug(self):
        title1 = "pruba de slug 10"
        title2 = "pruba de slug 20"
        title3 = "pruba de slug 30"
        slug1 = slugify(title1)
        slug2 = slugify(title2)
        slug3 = slugify(title3)
        obj1 = self.create_post(title=title1)
        obj2 = self.create_post(title=title2)
        obj3 = self.create_post(title=title3)
        self.assertEqual(obj1.slug, slug1)
        self.assertEqual(obj2.slug, slug2)
        self.assertNotEqual(obj3.slug, slug2)
        print("test model slug")
    
    def test_post_qs(self):
        title1 = "pruba de slug 100"
        obj1 = self.create_post(title=title1)
        # Query set title
        qs = PostModel.objects.filter(title=title1)
        self.assertEqual(qs.count(), 1)
        # Query set slug
        qs2 = PostModel.objects.filter(slug=obj1.slug)
        self.assertEqual(qs2.count(), 1)
        print("test model qs")