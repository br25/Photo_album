from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import UserSerializer, LoginSerializer, LogoutSerializer
from .tokens import generate_tokens
from django.urls import reverse


class UserView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        queryset = User.objects.all()
        if self.request.query_params.get('is_verified'):
            is_verified = self.request.query_params.get('is_verified').lower() == 'true'
            queryset = queryset.filter(is_verified=is_verified)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serialized_data = self.get_serializer(queryset, many=True).data

        for data in serialized_data:
            data['full_name'] = f"{data['first_name']} {data['last_name']}"

        return Response(serialized_data, status=status.HTTP_200_OK)


class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)  # Log in the user
            # Generate the full login URL
            login_url = request.build_absolute_uri(reverse('login'))

            tokens = generate_tokens(user)
            # Perform any additional actions or authentication-related tasks here
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            # Perform any logout-related tasks here
            logout(request)  # Log out the user
            return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
