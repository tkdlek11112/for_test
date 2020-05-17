from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
import requests
from .serializers import CreateUserSerializer
from .models import User
from django.core.paginator import Paginator

CLIENT_ID = 'zKBV4JsyllGOE7avU1KHw4wW2QSb1foqAo4fc41q'
CLIENT_SECRET = 'kC70k1jLfCDlOgRRaDNX6Qr1YU7xB2NFhvCw9tP8yLQHPNwydSfnhz2zmbrwVI7l1asojV7eHM75xWSrUR9TRDfHFV2Tar1ZO99VPufoGug9f1W9YU9NCzwOpBQVpQPc'


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        r = requests.post(
            'http://127.0.0.1:8000/o/token/',
            data={'grant_type': 'password',
                  'username': request.data['email'],
                  'password': request.data['password'],
                  'client_id': CLIENT_ID,
                  'client_secret': CLIENT_SECRET,
                  },
        )
        return Response(r.json())
    return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    r = requests.post(
        'http://127.0.0.1:8000/o/token/',
        data={
            'grant_type': 'password',
            'username': request.data['email'],
            'password': request.data['password'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    r = requests.post(
        'http://127.0.0.1:8000/o/token/',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': request.data['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    r = requests.post(
        'http://127.0.0.1:8000/o/revoke_token/',
        data={
            'token': request.data['token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    if r.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'}, r.status_code)
    return Response(r.json(), r.status_code)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    return Response({'code': '0', 'message': 'success'}, requests.codes.ok)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def info(request):
    in_email = request.GET.get('email', '')
    print(in_email)
    data = User.objects.filter(email=in_email).values('name', 'nickname', 'phone', 'gender', 'last_order_num', 'last_product_name', 'last_order_date').first()
    if data is None:
        return Response({'code':'9999', 'message':'사용자를 찾을 수 없습니다.'}, requests.codes.ok)

    return Response(data, requests.codes.ok)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def info_list(request):
    page_num = request.GET.get('page_num', None)
    per_page = request.GET.get('per_page', None)

    if page_num is None or per_page is None:
        return

    in_email = request.GET.get('email', None)
    name = request.GET.get('name', None)

    users = User.objects.all()

    if in_email is not None:
        users = users.filter(email=in_email)
    if name is not None:
        users = users.filter(name=name)
    per_page = int(per_page)
    page_num = int(page_num)
    offset = page_num * per_page
    users = list(users.values())
    if len(users) >= offset + per_page:
        users = users[offset: offset + per_page]
    elif len(users) >= offset:
        users = users[offset:]
    else:
        return Response({'code':9999,'message':'페이지 처리 에러'}, requests.codes.ok)

    return JsonResponse(users, safe=False)
