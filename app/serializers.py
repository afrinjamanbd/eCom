from app.models import ProductTable, ExtendUser
from rest_framework import serializers

# serializer class for third party users
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductTable 
        fields=('id','name','description', 'price', 'image')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtendUser
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance