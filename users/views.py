# Django
from users.models import Cliente, Gasto, Categoria
from django.db.models import Count, Sum

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


def get_resumen(url, headers, cliente, periodo):
    
    try:
        result = (Gasto.objects
            .filter(cliente=cliente)
            .values('categoria__nombre')
            .annotate(monto=Sum('monto'))
            .order_by()
        )
      
        mensaje = []
        for i in result:
            print(f'{i["categoria__nombre"]} - {i["monto"]}')
            mensaje.append(f'{i["categoria__nombre"]} - {i["monto"]}' + '\n')

        s=""""""

        for m in mensaje:
            s += m         


        payload = {"body": [
            {
                "type": "text",
                "text": f'{s}'
            }
        ]}
    except:
        payload = {"body": [
            {
                "type": "text",
                "text": "No pudiomos obtener el resumen de sus gastos."
            }
        ]}

    response = requests.request("POST", url, json=payload, headers=headers)

    return Response(status=response.status_code)
    # return Response(status=200)


class list_parameters(views.APIView):

    def post(self, request):
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        print('   ')
        print('   ')
        print('   ')
        print('   ')
        print('   ')
        print('   ')
        print('   ')
        print('   ')
        print('   ')
        print('   ')
        print('   ')
        print('   ')
        print(request.data)
        telegram_token = '3de05bd610c883cae1c7f27c924071543ce73662f0319b996f9f6991176b9e6a5a649f9962137504b68b0b66f1cfe6434e5151809a314ea1c0651c4fcb4be208'
        ws_token = 'efaa72594d1aa8a7122be3c49b65c8a7b65f4b943744c79015eb0c64689500b28d4fd15a435a0b5ff7802c1c963abde3983786e9a83a027954d448cfd898729d'

        headers = {
            "Authorization": f'Bearer {ws_token}',
            "Content-Type": "application/json"
        }

        resumen = True if 'action' in request.data['queryResult'] else False

        if resumen == False:
            category = request.data['queryResult']['parameters']['category']
            # currency = request.data['queryResult']['parameters']['currency']
            monto = request.data['queryResult']['parameters']['number']
            mensaje = request.data['queryResult']['queryText']

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
        else:
            periodo_reporte = request.data['queryResult']['parameters']['periodo-reporte']


        contact_id = request.data['originalDetectIntentRequest']['payload']['contact']['cId']
        # nombre = request.data['originalDetectIntentRequest']['payload']['body']['message']['chat']['first_name']
        nombre = request.data['originalDetectIntentRequest']['payload']['body']['contacts'][0]['profile']['name']
        # apellido = request.data['originalDetectIntentRequest']['payload']['body']['message']['chat']['last_name']



        url = f'https://app.botcity.com.do/api/v1/message/sendContent/{contact_id}'

        # Obtener o crear cliente
        try:
            cliente = Cliente.active.get(botcity_id=contact_id)
        except:
            cliente = Cliente()
            cliente.nombre = nombre or ''
            cliente.botcity_id = contact_id
            cliente.save()


                

        if resumen:
            get_resumen(url, headers, cliente, periodo_reporte)
        else:
            registrar_gasto(url, headers, cliente, categoria, monto, mensaje)


        return Response(status=200)
