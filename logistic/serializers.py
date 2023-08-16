from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['stock','product','quantity','price']

class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'products','positions']

    def create(self, validated_data):
        # ������� ��������� ������ ��� ������ ������
        positions = validated_data.pop('positions')

        # ������� ����� �� ��� ����������
        stock = super().create(validated_data)

        # ����� ��� ���� ��������� ��������� �������
        # � ����� ������: ������� StockProduct
        # � ������� ������ positions
        product = Stock.objects.create(**validated_data)
        StockProduct.objects.create(product=product, **positions)

        return stock
    

    