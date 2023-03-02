import logging

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from user.serializers import RegistrationSerializer, LoginSerializer


logging.basicConfig(filename="user_regi.log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


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

    def create(self, request, *args, **kwargs):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            login(request, serializer.context.get("user"))
            return Response({"Message": "User Login Successfully", "status": 201})
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)


class LogoutAPI(APIView):

    # @login_required
    def get(self, request):
        logout(request)
        return Response({"Message": "Logout Successfully"})

