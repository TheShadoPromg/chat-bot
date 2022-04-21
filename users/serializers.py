from telnetlib import GA
from rest_framework import serializers

from users.models import Gasto, Categoria


class GastoSerializer(serializers.ModelSerializer):
    categoria=serializers.SlugRelatedField(slug_field='unique_id', queryset=Categoria.objects.all())

    class Meta:
        model=Gasto
        fields= '__all__'