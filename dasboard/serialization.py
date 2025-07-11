from rest_framework.serializers import Serializer
from .models import Luxury_car
from rest_framework.serializers import ModelSerializer



class CarSerializer(ModelSerializer):

    class Meta:
        model = Luxury_car
        fields = ("name","price","description")


    
    