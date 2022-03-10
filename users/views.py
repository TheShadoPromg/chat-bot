# Django
from django.http.response import JsonResponse

# DRF
from rest_framework import views


class list_parameters(views.APIView):

    def post(self, request):
        result = []

        category = request.data['queryResult']['parameters']['category']
        currency = request.data['queryResult']['parameters']['currency']
        number = request.data['queryResult']['parameters']['number']

        result.append({
            "cetegoria": category,
            "moneda": currency,
            "monto": number
        })

        return JsonResponse(result, safe=False)
