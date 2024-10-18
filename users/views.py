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
    
import random
import string
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Agency
from .serializers import AgencySerializer
from rest_framework.permissions import IsAuthenticated

def generate_random_password(length=8):
    # Generate a random password of specified length
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class CreateAgencyView(generics.CreateAPIView):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Generate a random password
        random_password = generate_random_password()

        # Set the created_by field to the current user
        agency = serializer.save(created_by=self.request.user)

        # Optionally, if you want to create a user account for the agency:
        user = User.objects.create_user(username=agency.name, password=random_password)
        
        # Return the agency data along with the generated password
        return Response({
            'agency': serializer.data,
            'password': random_password
        }, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.perform_create(serializer)
