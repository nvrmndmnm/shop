from storefront.models import Category


def menu_processor(request):
    categories_list = Category.objects.exclude(is_parent=True)
    return {'categories_list': categories_list}
