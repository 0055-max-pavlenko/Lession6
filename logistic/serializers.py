from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product','quantity','price']

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
        for position in positions:
            print(position)
           # StockProduct.objects.create(stock = position.stock, product = position.product,
                #quantity = position.quantity, price = position.price)
            #product = Stock.objects.create(**validated_data)
            #StockProduct.objects.create(product=product, **position)
        
        return stock
    
    def update(self, instance, validated_data):
       # ������� ��������� ������ ��� ������ ������
       positions = validated_data.pop('positions')

       # ��������� ����� �� ��� ����������
       stock = super().update(instance, validated_data)

       # ����� ��� ���� �������� ��������� �������
       # � ����� ������: ������� StockProduct
       # � ������� ������ positions

       return stock
    