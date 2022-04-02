from django.contrib import admin
from users.models import Cliente, Categoria, Gasto

admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Gasto)