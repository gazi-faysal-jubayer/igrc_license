from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.middleware.csrf import get_token

def csrf_token_view(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})


@api_view(['POST'])
def signup_superuser(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please provide username and password'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the superuser
        User.objects.create_superuser(username=username, password=password)
        return Response(True, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_superuser(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please provide username and password'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_superuser:
            login(request, user)
            return Response(True, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not a superuser'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Agency
from .serializers import AgencySerializer

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_agency_view(request):
    if request.method == 'POST':
        serializer = AgencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


