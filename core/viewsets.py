from abc import ABC

from rest_framework import viewsets



class BaseViewSet(viewsets.ModelViewSet, ABC):
    lookup_field = 'unique_id'
    http_method_names = ['get', 'post', 'patch', 'delete']