from django.db import models
from datetime import date

from core.models import BaseModel


class Cliente(BaseModel):

    @staticmethod
    def get_reference_type():
        return 'CLI'

    class Meta:
        verbose_name = ('Cliente')
        verbose_name_plural = ('Clientes')


    nombre = models.CharField(verbose_name=('Nombre'), max_length=100)
    botcity_id = models.CharField(verbose_name=('Bot city id'), max_length=100)
    numero = models.CharField(verbose_name=('Numero'), max_length=50, blank=True, null=True)
    correo = models.CharField(verbose_name=('Correo'), max_length=100, blank=True, null=True)


    def __str__(self):
        return self.nombre


class Categoria(BaseModel):

    @staticmethod
    def get_reference_type():
        return 'CAT'

    class Meta:
        verbose_name = ('Categoria')
        verbose_name_plural = ('Categorias')


    nombre = models.CharField(verbose_name=('Nombre'), max_length=100)
    descripcion = models.CharField(verbose_name=('Descripcion'), max_length=200, blank=True, null=True)


    def __str__(self):
        return self.nombre


class Gasto(BaseModel):

    @staticmethod
    def get_reference_type():
        return 'GAS'

    class Meta:
        verbose_name = ('Gasto')
        verbose_name_plural = ('Gastos')


    cliente = models.ForeignKey('Cliente',verbose_name=('Cliente'), on_delete=models.PROTECT)
    categoria = models.ForeignKey('Categoria',verbose_name=('Categoria'), on_delete=models.PROTECT)
    monto = models.PositiveBigIntegerField(verbose_name=('Monto'), default=0)
    fecha = models.DateField(verbose_name=('Fecha'), default=date.today())
    concepto = models.CharField(verbose_name=('Concepto'), max_length=200, blank=True, null=True)


    def __str__(self):
        return f'{self.cliente.nombre}-{self.categoria.nombre}'