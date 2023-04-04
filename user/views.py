import logging

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
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



class Registration(viewsets.ModelViewSet):
    """
    Class for user registration
    """
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(request_body=RegistrationSerializer, operation_summary='Post UserRegistrations')
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


@csrf_exempt
def user_registration(request):
    """
    Function for registering user
    """
    try:
        if request.method == 'GET':
            return render(request, 'user/registration.html')

        if request.method == 'POST':
            obj = request.POST
            User.objects.create_user(first_name=obj.get('first_name'), last_name=obj.get('last_name'),
                                            username=obj.get('username'), password=obj.get('password'),
                                            email=obj.get('email'), mob_num=obj.get('mob_num'),
                                            location=obj.get('location'))
            return redirect("user_login")
        # messages.info(request, "You have successfully registered.")
        return render(request, 'user/registration.html')

    except Exception as e:
        logging.error(e)
        return render(request, 'user/registration.html')


@csrf_exempt
def user_login(request):
    """
    Function for user login
    """
    try:
        if request.method == 'GET':
            return render(request, 'user/login.html')

        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_authenticated:
                    return redirect("home_page")
                else:
                    return redirect("user_login")
            else:
                return HttpResponse('login required')
        return render(request, 'user/login.html')

    except Exception as e:
        logging.error(e)
        return render(request, 'user/login.html')


@csrf_exempt
@login_required
def home_page(request):
    """
    Function for home page
    """
    try:
        print(request.user.id)
        if request.method == 'GET':
            user = User.objects.get(id=request.user.id)
            return render(request, 'user/home_page.html', {'user': user})
    except Exception as e:
        logging.error(e)
        return render(request, 'user/home_page.html')


@csrf_exempt
@login_required
def user_logout(request):
    """
    Function for user logout
    """
    try:
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect("user_login")
    except Exception as e:
        logging.error(e)
