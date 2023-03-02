import logging

from django.contrib.auth import authenticate
from rest_framework import serializers

from user.models import User

logging.basicConfig(filename="serializer.log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Class for user registration serializer
    """

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'mob_num', 'location']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        try:
            return User.objects.create_user(**validated_data)
        except Exception as e:
            logging.error(e)


class LoginSerializer(serializers.Serializer):
    """
     Class for user login serializer
    """
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)

    def create(self, validated_data):
        user = authenticate(**validated_data)
        if not user:
            raise Exception('Invalid Credentials')
        self.context.update({"user": user})
        return user
