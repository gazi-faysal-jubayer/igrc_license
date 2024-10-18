from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.authtoken.models import Token

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
from django.contrib.auth.models import User
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
        # Generate a random password for the agency user
        random_password = generate_random_password()

        # Save the agency and link it to the creator
        agency = serializer.save(created_by=self.request.user)

        # Create a user account for the agency with the generated password
        user = User.objects.create_user(
            username=agency.name,  # or another unique identifier
            password=random_password,
            email=agency.email  # Use agency email if available
        )

        # Return the agency data along with the generated password
        return Response({
            'agency': serializer.data,
            'password': random_password,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.perform_create(serializer)


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class AgencyLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'email': user.email
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgencyListView(APIView):
    def get(self, request):
        agencies = Agency.objects.all()
        serializer = AgencySerializer(agencies, many=True)
        return Response(serializer.data)
    
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import License
from .serializers import LicenseSerializer

class LicenseListView(APIView):
    def get(self, request):
        licenses = License.objects.all()
        serializer = LicenseSerializer(licenses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LicenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LicenseDetailView(APIView):
    def get(self, request, pk):
        try:
            license = License.objects.get(pk=pk)
        except License.DoesNotExist:
            return Response({'error': 'License not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LicenseSerializer(license)
        return Response(serializer.data)
