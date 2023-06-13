from app.models import ProductTable
from rest_framework import serializers

# serializer class for third party users
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductTable 
        fields=('id','name','description', 'price', 'image')
