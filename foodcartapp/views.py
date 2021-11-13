from django.http import JsonResponse
from django.templatetags.static import static
import json
from pprint import pprint
from .models import Order
from .models import OrderMenuItem
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import Product


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    Order.objects.create(address=request.data["address"],
                         firstname=request.data["firstname"],
                         lastname=request.data["lastname"],
                         phonenumber=request.data["phonenumber"]
                         )
    order = Order.objects.get(firstname=request.data["address"],
                              lastname=request.data["firstname"],
                              address=request.data["lastname"],
                              phonenumber=request.data["phonenumber"]
                              )
    for product in request.data["products"]:
        product_id = product["product"]
        quantity = product["quantity"]
        prod = Product.objects.get(pk=product_id)
        OrderMenuItem.objects.create(order=order, product=prod, quantity=quantity)
    return Response(request.data)

