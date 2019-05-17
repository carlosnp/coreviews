# Django
from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

# Project
from blog.models import PostModel
from blog.forms import PostModelForm


class PostModelFormTestCase(TestCase):
    def test_valid_form(self):
        title   ='Titulo de prueba del formulario 1'
        slug = slugify(title)
        content ='Contetido lorem ipsum'
        publish = 'publish'
        # Crea en base de datos
        # obj   = PostModel.objects.create(
        #     title=title,
        #     # slug=slug,
        #     publish=publish,
        #     content=content,
        # )
        # data = {
        #     'title':obj.title,
        #     'slug':obj.slug,
        #     'publish':obj.publish,
        #     'content':obj.content,
        # }
        data = {
            'title':title,
            # 'slug':obj.slug,
            'publish':publish,
            'content':content,
        }
        form = PostModelForm(data=data)
        # Verificamos que el formulario sea valido
        self.assertTrue(form.is_valid())
        # Si hay errores los imprime
        if form.errors:
            print("")
            print("errors valid form")
            print(form.errors)
            print("")
        self.assertEqual(
            form.cleaned_data.get("title"),
            title
        )
        self.assertNotEqual(
            form.cleaned_data.get("content"),
            "Hola mundo"
        )
        print("test valid form")

    def test_invalid_form(self):
        title   ='Titulo de prueba del formulario 1'
        slug = slugify(title)
        content ='Contetido lorem ipsum'
        publish = 'publish'
        # Crea en base de datos
        obj   = PostModel.objects.create(
            title=title,
            # slug=slug,
            publish=publish,
            content=content,
        )
        data = {
            'title':obj.title,
            'slug':obj.slug,
            'publish':obj.publish,
            'content':obj.content,
        }
        # En el formulario se coloca informacion 
        # ya existente en base de datos
        form = PostModelForm(data=data)
        if form.errors:
            print("")
            print("errors invalid form")
            print(form.errors)
            print("")
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        print("test invalid form")