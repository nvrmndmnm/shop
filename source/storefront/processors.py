from django.contrib.auth.decorators import login_required

from cart.models import Order
from storefront.models import Category


def menu_processor(request):
    categories_list = Category.objects.exclude(is_parent=True)
    return {'categories_list': categories_list}


def cart_items(request):
    if request.user.is_authenticated:
        items = Order.objects.filter(user=request.user, status='NEW', items__isnull=False).first()
        return {'cart_items': items}
    return {'cart_items': None}
