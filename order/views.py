from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Order



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
    in_email = request.GET.get('email', '')
    orders = list(Order.objects.filter(email=in_email).values())
    # data = serializers.serialize('json', orders)

    return JsonResponse(orders, safe=False)
