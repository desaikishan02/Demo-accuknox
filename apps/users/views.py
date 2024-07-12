from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.serializers import RegisterSerializer, MyTokenObtainPairSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserPagination(PageNumberPagination):
    page_size = 10


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = UserPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search_keyword = self.request.query_params.get('search', '')
        return User.objects.filter(
            Q(email__iexact=search_keyword) | Q(first_name__icontains=search_keyword)
        )
