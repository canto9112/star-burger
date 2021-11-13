from rest_framework.serializers import ModelSerializer

from .models import Order, OrderMenuItem


class OrderProductsSerializer(ModelSerializer):
    class Meta:
        model = OrderMenuItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderProductsSerializer(many=True, allow_empty=False, write_only=True)

    class Meta:
        model = Order
        fields = ['address', 'firstname', 'lastname', 'phonenumber', 'products']
