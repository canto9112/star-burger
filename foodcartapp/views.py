from django.http import JsonResponse
from django.templatetags.static import static
import json
from pprint import pprint
from .models import Order
from .models import OrderMenuItem
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.serializers import Serializer
from rest_framework.serializers import CharField, ListSerializer
from rest_framework.serializers import ModelSerializer


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

# def validate(data):
#     errors = []
#
#     if 'products' not in data:
#         errors.append('Подуктов нет. products: Обязательное поле.')
#     check_product = isinstance(data['products'], list)
#     if check_product is False:
#         errors.append(f'''products: Ожидался list со значениями, но был получен "{type(data['products'])}".''')
#     if not data['products']:
#         errors.append('Продукты — пустой список. products: Этот список не может быть пустым.')
#


class OrderProductsSerializer(ModelSerializer):
    class Meta:
        model = OrderMenuItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderProductsSerializer()

    class Meta:
        model = Order
        fields = ['address', 'firstname', 'lastname', 'phonenumber', 'products']


@api_view(['POST', ])
def register_order(request):
    data = request.data

    order_serializer = OrderSerializer(data=request.data)
    order_serializer.is_valid(raise_exception=True)

    order = Order.objects.create(firstname=data['firstname'],
                                 lastname=data['lastname'],
                                 address=data['address'],
                                 phonenumber=data['phonenumber']
                                 )

    for item in data['products']:
        order.order_items.create(product_id=item['product'], quantity=item['quantity'])

    return Response(data, status=status.HTTP_201_CREATED)

