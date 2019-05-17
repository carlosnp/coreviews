# Django
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

# Project
from blog.models import PostModel
from blog.forms import PostModelForm

class PostModelTestViewCase(TestCase):
    def create_post(self, title="Test Views"):
        return PostModel.objects.create(title=title)
    
    def test_list_view(self):
        list_url = reverse("posts:list")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)
        print("Test ListView")

    def test_detail_view(self):
        title   ='Test DetailView'
        content ='Contenido lorem ipsum'
        publish = 'publish'
        # Crea en base de datos un post
        obj   = PostModel.objects.create(
                title   = title,
                publish = publish,
                content = content,
        )
        response = self.client.get(obj.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        print("Test DetailView")
    
    def test_updated_view(self):
        title   ='Test UpdateView 1'
        content ='Contenido lorem ipsum'
        publish = 'publish'
        # Crea en base de datos un post
        obj   = PostModel.objects.create(
                title   = title,
                publish = publish,
                content = content,
        )
        update_url = reverse("posts:update", kwargs={"pk":obj.pk})
        if update_url:
            print()
            print("Update View data")
            print(update_url)
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)
        print("Test UpdateView")
    
    def test_delete_view(self):
        title   ='Test DeteleView 1'
        content ='Contenido lorem ipsum'
        publish = 'publish'
        # Crea en base de datos un post
        obj   = PostModel.objects.create(
                title   = title,
                publish = publish,
                content = content,
        )
        delete_url = reverse("posts:delete", kwargs={"pk":obj.pk})
        # if delete_url:
        #     print()
        #     print("Delete View data")
        #     print(delete_url)
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
        print("Test DeleteView")
