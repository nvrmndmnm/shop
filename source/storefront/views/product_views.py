from django.shortcuts import render
from django.views.generic import View, ListView


class IndexView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, "index.html")
