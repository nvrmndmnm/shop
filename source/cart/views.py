from django.http import HttpResponseRedirect
from django.shortcuts import render




def add_to_cart(request):
    print("pass")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
