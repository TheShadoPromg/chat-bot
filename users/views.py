# Django
from users.models import Cliente, Gasto, Categoria

# DRF
from rest_framework import views
from rest_framework.response import Response

# others
import requests


def registrar_gasto(url, headers, cliente, categoria, monto, mensaje):

    try:
        gasto = Gasto()
        gasto.cliente = cliente
        gasto.categoria = categoria
        gasto.monto = monto
        gasto.concepto = mensaje
        gasto.save()

        payload = {"body": [
            {
                "type": "text",
                "text": f'Su gasto de {monto} ha sido registrado en la categoria {categoria}.'
            }
        ]}
    except:
        payload = {"body": [
            {
                "type": "text",
                "text": "No pudiomos registrar su gasto."
            }
        ]}

    response = requests.request("POST", url, json=payload, headers=headers)

    return Response(status=response.status_code)


class list_parameters(views.APIView):

    def post(self, request):
        # print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        # print(request.data)
        telegram_token = '3de05bd610c883cae1c7f27c924071543ce73662f0319b996f9f6991176b9e6a5a649f9962137504b68b0b66f1cfe6434e5151809a314ea1c0651c4fcb4be208'

        headers = {
            "Authorization": f'Bearer {telegram_token}',
            "Content-Type": "application/json"
        }

        category = request.data['queryResult']['parameters']['category']
        # currency = request.data['queryResult']['parameters']['currency']
        monto = request.data['queryResult']['parameters']['number']
        mensaje = request.data['queryResult']['queryText']
        contact_id = request.data['originalDetectIntentRequest']['payload']['contact']['cId']
        nombre = request.data['originalDetectIntentRequest']['payload']['body']['message']['chat']['first_name']
        # apellido = request.data['originalDetectIntentRequest']['payload']['body']['message']['chat']['last_name']

        url = f'https://app.botcity.com.do/api/v1/message/sendContent/{contact_id}'

        # Obtener o crear cliente
        try:
            cliente = Cliente.active.get(botcity_id=contact_id)
        except:
            cliente = Cliente()
            cliente.nombre = nombre
            cliente.botcity_id = contact_id
            cliente.save()

        # Obtener o crear categoria
        if isinstance(category, list):
            category = category[0]
            try:
                categoria = Categoria.active.get(nombre=category)
            except:
                categoria = Categoria()
                categoria.nombre = category
                categoria.save()
        else:
            try:
                categoria = Categoria.active.get(nombre=category)
            except:
                categoria = Categoria()
                categoria.nombre = category
                categoria.save()
                

        registrar_gasto(url, headers, cliente, categoria, monto, mensaje)


        return Response(status=200)
