# Django
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.base import TemplateResponseMixin, ContextMixin

# Home Page
class HomeView(TemplateView):
    template_name = "home.html"

    # Context Data
    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args,**kwargs)
        context["title"] = "Home Page"
        context["content"] = "Duis veniam velit dolor ex aute in magna. Ullamco mollit nisi ea cillum do laborum eu. Tempor sunt sint ipsum velit id deserunt cupidatat cillum est pariatur ex. Tempor elit fugiat commodo aliquip elit nisi incididunt consequat minim. Voluptate non pariatur sit dolor adipisicing aute minim ipsum veniam ex nostrud cillum eiusmod. Laborum exercitation consequat elit consequat non nostrud. Fugiat cillum esse ullamco minim aute minim ex do exercitation veniam."
        return context
# About
class AboutView(TemplateResponseMixin, ContextMixin, View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['title'] = 'About'
        context['content'] = 'Laborum cupidatat incididunt est dolore. Irure id ea elit id ea nulla tempor commodo duis sit. Et proident eiusmod occaecat minim quis magna laborum exercitation exercitation Lorem officia. Quis enim ea non cillum tempor ex exercitation non nostrud. Sint reprehenderit id irure incididunt. Velit aliqua cillum dolore officia magna aliquip fugiat cupidatat magna est. Amet et adipisicing veniam laboris mollit aliqua occaecat. Aliquip nostrud proident est cillum ad nisi Lorem sint dolore duis pariatur sit. Sunt incididunt dolor minim occaecat sit magna. Consectetur veniam voluptate laborum ea consequat eu fugiat sit amet duis adipisicing officia. Dolore qui cupidatat sint incididunt ullamco ut irure adipisicing velit elit dolor. Id enim eiusmod sunt est labore adipisicing sint quis dolor quis. Tempor et do cillum nisi ad pariatur incididunt.'
        return self.render_to_response(context)