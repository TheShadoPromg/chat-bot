from rest_framework import viewsets

from users.models import Gasto

from users.serializers import GastoSerializer

class GastoViewSet(viewsets.ModelViewSet):
    lookup_field = 'unique_id'
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Gasto.objects.all()
    serializer_class = GastoSerializer
