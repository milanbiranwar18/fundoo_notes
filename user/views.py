import logging

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from user.serializers import RegistrationSerializer, LoginSerializer
from user.utils import JWT

logging.basicConfig(filename="user_regi.log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


@swagger_auto_schema(request_body=RegistrationSerializer, operation_summary='Post UserRegistrations')
class Registration(viewsets.ModelViewSet):
    """
    Class for user registration
    """
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response({"Message": "User Registered Successfully", "data": response.data, "status":201})
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)


class Login(viewsets.ModelViewSet):
    """
     Class for user login
    """
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer, operation_summary='Post UserLogin')
    def create(self, request, *args, **kwargs):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            login(request, serializer.context.get("user"))
            user = serializer.context.get("user")
            token = JWT().encode(data={"user_id": user.id})
            return Response({"Message": "User Login Successfully", "token":token, "status": 201})
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)


class LogoutAPI(APIView):

    @swagger_auto_schema(operation_summary='GET User Logout')
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({"Message": "Logout Successfully", "status": 200})
        return Response({"Message": "User already logout"})

