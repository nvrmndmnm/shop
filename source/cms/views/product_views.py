from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    template_name = 'cms.html'

    def get(self, request, *args, **kwargs):
        return render(request, "cms.html")
