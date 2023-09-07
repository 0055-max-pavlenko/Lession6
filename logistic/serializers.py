from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product','quantity','price']

class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id','address', 'products','positions']

    def create(self, validated_data):
        # ������� ��������� ������ ��� ������ ������
        positions = validated_data.pop('positions')

        # ������� ����� �� ��� ����������
        stock = super().create(validated_data)

        # ����� ��� ���� ��������� ��������� �������
        # � ����� ������: ������� StockProduct
        # � ������� ������ positions
        for p in positions:
            stock.positions.create(**p)
        
        return stock
    
    def update(self, instance, validated_data):
       # ������� ��������� ������ ��� ������ ������
       positions = validated_data.pop('positions')

       # ��������� ����� �� ��� ����������
       stock = super().update(instance, validated_data)

       # ����� ��� ���� �������� ��������� �������
       # � ����� ������: ������� StockProduct
       # � ������� ������ positions
       for p in positions:
           stock.positions.update_or_create(product=p['product'], defaults={**p})

       return stock
    