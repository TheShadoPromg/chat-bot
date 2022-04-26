# Django
from users.models import Cliente, Gasto, Categoria, Ingreso
from django.db.models import Count, Sum
from django.utils import timezone


# DRF
from rest_framework import views
from rest_framework.response import Response

# others
import requests
from datetime import date, datetime, timedelta
from datetime import timedelta
from dateutil.relativedelta import relativedelta



def registrar_gasto(url, headers, cliente, categoria, monto, mensaje):
    print('gastos')

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


def registrar_ingreso(url, headers, cliente, categoria, monto):
    print('ingresos')

    try:
        if isinstance(monto, list):
            # print(monto)
            monto = monto[0]
        # print(monto)
        ingreso = Ingreso()
        ingreso.cliente = cliente
        ingreso.categoria = categoria
        ingreso.monto = monto
        ingreso.save()

        payload = {"body": [
            {
                "type": "text",
                "text": f'Su ingreso de {monto} ha sido registrado.'
            }
        ]}
    except:
        payload = {"body": [
            {
                "type": "text",
                "text": "No pudiomos registrar su ingreso."
            }
        ]}

    response = requests.request("POST", url, json=payload, headers=headers)

    return Response(status=response.status_code)
    # return Response(status=200)


def get_resumen(url, headers, cliente, periodo, tipo):
    print('resumen')

    if periodo == 'diario':
        periodo = date.today()
    elif periodo == 'semanal':
        periodo = timezone.now().date() - timedelta(days=7)
    elif periodo == 'quincenal':
        periodo = timezone.now().date() - timedelta(days=15)
    elif periodo == 'mensual':
        periodo = date.today() + relativedelta(months=-1)
    elif periodo == 'trimestral':
        periodo = date.today() + relativedelta(months=-3)


    if tipo == 'resumen-gastos':
        try:
            result = (Gasto.objects
                .filter(cliente=cliente, fecha__range=(periodo, date.today()))
                .values('categoria__nombre')
                .annotate(monto=Sum('monto'))
                .order_by()
            )
        
            mensaje = []
            for i in result:
                # print(f'{i["categoria__nombre"]} - {i["monto"]}')
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
                    "text": "No pudiomos obtener su resumen."
                }
            ]}
    elif tipo == 'resumen-ingresos':
        try:
            result = (Ingreso.objects
                .filter(cliente=cliente, fecha__range=(periodo, date.today()))
                .values('categoria__nombre')
                .annotate(monto=Sum('monto'))
                .order_by()
            )
        
            mensaje = []
            for i in result:
                # print(f'{i["categoria__nombre"]} - {i["monto"]}')
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
                    "text": "No pudiomos obtener su resumen."
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
        print(request.data)
        telegram_token = '3de05bd610c883cae1c7f27c924071543ce73662f0319b996f9f6991176b9e6a5a649f9962137504b68b0b66f1cfe6434e5151809a314ea1c0651c4fcb4be208'
        ws_token = 'efaa72594d1aa8a7122be3c49b65c8a7b65f4b943744c79015eb0c64689500b28d4fd15a435a0b5ff7802c1c963abde3983786e9a83a027954d448cfd898729d'
        ariel_token = 'f85ef8efec71f0e6c066f9cab1f20a4febad1c9d9f0fb08383b01a8976f7c2585be5edae6186399ec7a7da779074108a456b3038aef4187b0c73c822b1e6c4d6'

        headers = {
            "Authorization": f'Bearer {ariel_token}',
            "Content-Type": "application/json"
        }

        resumen = True if request.data['queryResult']['action'] == 'resumen-ingresos' or request.data['queryResult']['action'] == 'resumen-gastos' else False

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
        nombre = request.data['originalDetectIntentRequest']['payload']['body']['contacts'][0]['profile']['name']
        tipo = request.data['queryResult']['action']


        url = f'https://app.respond.io/api/v1/message/sendContent/{contact_id}'

        # Obtener o crear cliente
        try:
            cliente = Cliente.active.get(botcity_id=contact_id)
        except:
            cliente = Cliente()
            cliente.nombre = nombre or ''
            cliente.botcity_id = contact_id
            cliente.save()


        if resumen:
            get_resumen(url, headers, cliente, periodo_reporte, tipo)
        elif tipo == 'registro-gasto':
            registrar_gasto(url, headers, cliente, categoria, monto, mensaje)
        elif tipo == 'registro-ingresos':
            registrar_ingreso(url, headers, cliente, categoria, monto)


        return Response(status=200)
