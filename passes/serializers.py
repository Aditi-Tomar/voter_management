from rest_framework import serializers
from .models import PassRequest

class PassRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassRequest
        fields = ['name', 'email', 'phone', 'temple', 'persons', 'visit_date', 'id_proof']