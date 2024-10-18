from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

User = get_user_model()

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(email=email).exists():
            return Response({'detail': 'User with this email already exists in the database'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User(
            username = username,
            email = email,
            password = make_password(password)
        )

        user.save()

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'redirect_url': 'http://localhost:8000/api/login/',
            'token': token.key
        }, status=status.HTTP_201_CREATED)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(email=email, password=password)


        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({
                'user': UserSerializer(user).data,
                'redirect_url': 'http://localhost:8000/api/tasks/',
                'token': token.key
            })
                
        return Response({'detail': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
    
class UserLogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        try:
            token= request.auth
            token.delete()
            
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_204_NO_CONTENT)
        
        except (AttributeError, Token.DoesNotExist):
            return Response({'detail': 'Token not found or already logged out.'}, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
